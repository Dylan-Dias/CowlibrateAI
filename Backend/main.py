from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import asyncpg
import bcrypt
import jwt
import datetime
import json
import pulp  # import pulp as a whole for solver cmd access
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value


JWT_SECRET = "your_secret_key_here"

app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Database =====
async def get_db():
    return await asyncpg.connect("postgres://postgres:root@localhost:5432/CowlibrateAI")

# ===== Models =====
class User(BaseModel):
    username: str
    email: str
    password: str
    role: str

class Credentials(BaseModel):
    username: str
    password: str

class Animal(BaseModel):
    id: int | None = None
    milk_yield: float
    health: str
    breed: str
    lactation_stage: str
    age: int

class Feed(BaseModel):
    feed_type: str
    feed_quantity: float
    feed_percentage: float

class OptimizeRequest(BaseModel):
    goats: List[Animal]
    bovines: List[Animal]
    feeds: List[Feed]

# ===== User Routes =====
@app.post("/api/register")
async def register(user: User):
    if not all([user.username, user.email, user.password, user.role]):
        raise HTTPException(400, "Missing required fields")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    conn = await get_db()
    try:
        await conn.execute("""
            INSERT INTO users (username, email, password, role)
            VALUES ($1, $2, $3, $4)
        """, user.username, user.email, hashed_pw, user.role)
    finally:
        await conn.close()

    return {"message": "User registered successfully"}

@app.post("/api/login")
async def login(creds: Credentials):
    if not creds.username or not creds.password:
        raise HTTPException(400, "Missing credentials")

    conn = await get_db()
    try:
        row = await conn.fetchrow("SELECT password, role FROM users WHERE username=$1", creds.username)
    finally:
        await conn.close()

    if not row or not bcrypt.checkpw(creds.password.encode(), row["password"].encode()):
        raise HTTPException(401, "Invalid credentials")

    payload = {
        "username": creds.username,
        "role": row["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return {"token": token, "role": row["role"]}

# ===== Insert cows/goats + feeds =====
@app.post("/api/optimize")
async def optimize_insert(req: OptimizeRequest):
    conn = await get_db()
    try:
        # Goats
        for g in req.goats:
            goat_id = await conn.fetchval("""
                INSERT INTO goat_entries (milk_yield, health, breed, lactation_stage, age)
                VALUES ($1, $2, $3, $4, $5) RETURNING id
            """, g.milk_yield, g.health, g.breed, g.lactation_stage, g.age)

            for f in req.feeds:
                await conn.execute("""
                    INSERT INTO goat_feeds (goat_entry_id, feed_type, feed_quantity, feed_percentage)
                    VALUES ($1, $2, $3, $4)
                """, goat_id, f.feed_type, f.feed_quantity, f.feed_percentage)

        # Bovines
        for c in req.bovines:
            cow_id = await conn.fetchval("""
                INSERT INTO cow_entries (milk_yield, health, breed, lactation_stage, age)
                VALUES ($1, $2, $3, $4, $5) RETURNING id
            """, c.milk_yield, c.health, c.breed, c.lactation_stage, c.age)

            for f in req.feeds:
                await conn.execute("""
                    INSERT INTO cow_feeds (cow_entry_id, feed_type, feed_quantity, feed_percentage)
                    VALUES ($1, $2, $3, $4)
                """, cow_id, f.feed_type, f.feed_quantity, f.feed_percentage)
    finally:
        await conn.close()

    return {"message": "Optimization and storage complete"}

# ===== Optimization Algorithm =====
def run_optimization(bovines: List[dict], feeds: List[dict]):
    if not bovines:
        return []

    feed_impact = {
        f['feed_type']: 1 + (f['feed_percentage'] / 100) * 0.1
        for f in feeds
    }

    prob = LpProblem("Maximize Milk Yield", LpMaximize)
    cow_vars = {
        cow['id']: LpVariable(f"cow_{cow['id']}", cat='Binary')
        for cow in bovines
    }

    prob += lpSum([
        cow_vars[cow['id']] * cow['milk_yield'] * feed_impact.get(cow['breed'], 1.0)
        for cow in bovines
    ])

    prob += lpSum([cow_vars[cow['id']] for cow in bovines]) <= 10
    prob += lpSum([
        cow_vars[cow['id']] * (1 if cow['health'].lower() == 'healthy' else 0)
        for cow in bovines
    ]) >= 1

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    selected = [
        {
            'id': cow['id'],
            'milk_yield': cow['milk_yield'],
            'health': cow['health'],
            'breed': cow['breed'],
            'lactation_stage': cow['lactation_stage'],
            'age': cow['age']
        }
        for cow in bovines
        if value(cow_vars[cow['id']]) == 1
    ]

    return selected

# ===== API to fetch + optimize =====
@app.get("/api/optimize-run/{animal_type}")
async def optimize_run(animal_type: str):
    if animal_type == "cows":
        entries_table, feeds_table = "cow_entries", "cow_feeds"
    elif animal_type == "goats":
        entries_table, feeds_table = "goat_entries", "goat_feeds"
    else:
        raise HTTPException(400, "Invalid animal type")

    conn = await get_db()
    try:
        animals = await conn.fetch(f"SELECT id, milk_yield, health, breed, lactation_stage, age FROM {entries_table}")
        feeds = await conn.fetch(f"SELECT feed_type, feed_quantity, feed_percentage FROM {feeds_table}")
    finally:
        await conn.close()

    animals = [dict(a) for a in animals]
    feeds = [dict(f) for f in feeds]

    result = run_optimization(animals, feeds)
    return {"selected_cows": result}
