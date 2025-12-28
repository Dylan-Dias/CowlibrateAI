# server.py (refactored - Flask + psycopg2)
import os
import json
import logging
import datetime
from functools import wraps

import bcrypt
import jwt
import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# load env
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET not set in environment (.env)")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment (.env)")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174"]}})

# Mail config (optional)
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
mail = Mail(app)

limiter = Limiter(get_remote_address, app=app)
logging.basicConfig(level=logging.INFO)


def get_db_connection():
    """Return a new psycopg2 connection (use RealDictCursor when helpful)."""
    return psycopg2.connect(DATABASE_URL)


# -------------------------
# Auth helpers
# -------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = None
        if auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]
        if not token:
            return jsonify({"error": "Token missing"}), 401
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id = data.get("user_id")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except Exception:
            return jsonify({"error": "Invalid token"}), 401

        return f(user_id, *args, **kwargs)
    return decorated


# -------------------------
# Basic auth routes (unchanged)
# -------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (username, email, hashed, role))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.exception("Register failed")
        return jsonify({"error": "Registration failed", "detail": str(e)}), 500

    token = jwt.encode({
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "token": token,
        "user": {"id": user_id, "username": username, "email": email, "role": role}
    }), 201


@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logout successful"}), 200


@limiter.limit("5 per minute")
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash, role FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        logging.exception("DB error on login")
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    user_id, password_hash, role = user
    if bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
        token = jwt.encode({
            "user_id": user_id,
            "role": role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, JWT_SECRET, algorithm="HS256")
        return jsonify({"success": True, "message": "Login successful", "user_id": user_id, "role": role, "token": token})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


# -------------------------
# POST /api/optimize
# - saves a submission (as before)
# - runs optimization logic
# - stores selected_cows rows and an optimization_results summary JSON
# -------------------------
@app.route("/api/optimize", methods=["POST"])
@token_required
def optimize(user_id):
    data = request.get_json() or {}

    bovines = data.get("bovines", [])
    feeds = data.get("feeds", [])
    indoor_temp = data.get("indoor_temp")
    outdoor_temp = data.get("outdoor_temp")
    water_intake = data.get("water_intake")
    budget = data.get("budget")
    protein = data.get("protein")
    butterfat = data.get("butterfat")
    somatic_cell_count = data.get("somatic_cell_count")

    if not isinstance(bovines, list) or len(bovines) == 0:
        return jsonify({"error": "bovines must be a non-empty list"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Save submission (same as earlier)
        cur.execute("""
            INSERT INTO submissions
            (user_id, bovines, feeds, indoor_temp, outdoor_temp, water_intake, budget, protein, butterfat, somatic_cell_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at
        """, (
            user_id,
            json.dumps(bovines),
            json.dumps(feeds),
            indoor_temp,
            outdoor_temp,
            water_intake,
            budget,
            protein,
            butterfat,
            somatic_cell_count
        ))
        row = cur.fetchone()
        submission_id, created_at = row
        conn.commit()
    except Exception as e:
        logging.exception("Failed to save submission")
        # ensure connection closed on error
        try:
            cur.close()
            conn.close()
        except Exception:
            pass
        return jsonify({"error": "Failed to save submission", "detail": str(e)}), 500

    # ------- run the optimization (placeholder logic) -------
    # Replace this block with your real algorithm
    optimized = []
    for b in bovines:
        # safe extraction with defaults
        cow_id = b.get("id")
        age = b.get("age")
        breed = b.get("breed")
        health = b.get("health")
        milk_yield = b.get("milk_yield")
        lactation_stage = b.get("lactation_stage")

        # demo score: combine milk yield and age (placeholder)
        score = None
        try:
            # example deterministic score (0-100). Replace with real logic.
            base = float(milk_yield or 0)
            score = round(min(100, max(0, base * 3 - (age or 0) * 0.5)))
        except Exception:
            score = 0

        optimized.append({
            "bovine_id": cow_id,
            "age": age,
            "breed": breed,
            "health": health,
            "milk_yield": milk_yield,
            "lactation_stage": lactation_stage,
            "score": score
        })

    # ------- persist selected_cows and optimization_results -------
    try:
        cur = conn.cursor()
        # Insert each optimized cow as a row in selected_cows
        insert_sc_sql = """
            INSERT INTO selected_cows
            (submission_id, user_id, cow_id, age, breed, health, milk_yield, lactation_stage, score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for cow in optimized:
            cur.execute(insert_sc_sql, (
                submission_id,
                user_id,
                cow.get("bovine_id"),
                cow.get("age"),
                cow.get("breed"),
                cow.get("health"),
                cow.get("milk_yield"),
                cow.get("lactation_stage"),
                cow.get("score")
            ))

        # Insert an optimization_results summary (JSON)
        cur.execute("""
            INSERT INTO optimization_results (submission_id, user_id, results)
            VALUES (%s, %s, %s)
        """, (submission_id, user_id, json.dumps(optimized)))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.exception("Failed to persist optimized results")
        try:
            cur.close()
            conn.close()
        except Exception:
            pass
        return jsonify({"error": "Failed to persist optimization results", "detail": str(e)}), 500

    # Return the persisted results to the client (useful for immediate frontend render)
    return jsonify({
        "message": "Optimization completed and saved",
        "submission_id": submission_id,
        "timestamp": created_at.isoformat() if hasattr(created_at, "isoformat") else created_at,
        "results": optimized
    }), 201


# -------------------------
# GET /api/optimization-results
# Returns selected_cows for the latest submission for this user (persisted rows)
# -------------------------
@app.route("/api/optimization-results", methods=["GET"])
@token_required
def optimization_results(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Find latest submission_id for user from submissions table
        cur.execute("""
            SELECT id FROM submissions
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id,))
        srow = cur.fetchone()
        if not srow:
            cur.close()
            conn.close()
            return jsonify({"results": []}), 200

        latest_submission_id = srow['id']

        # Fetch selected_cows rows for that submission
        cur.execute("""
            SELECT cow_id, age, breed, health, milk_yield, lactation_stage, score, created_at
            FROM selected_cows
            WHERE submission_id = %s
            ORDER BY score DESC, created_at ASC
        """, (latest_submission_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # rows is a list of RealDictRow - json serializable
        return jsonify({"results": rows}), 200
    except Exception as e:
        logging.exception("Failed to fetch optimization results")
        return jsonify({"error": str(e)}), 500


# -------------------------
# Existing chart endpoints (live DB-backed) - unchanged behavior
# -------------------------
@token_required
@app.route("/health-distribution", methods=["GET"])
def health_distribution(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT bovine->> 'health' AS health, COUNT(*) AS cnt
            FROM submissions, jsonb_array_elements(COALESCE(bovines::jsonb, '[]'::jsonb)) AS bovine
            WHERE (bovine->> 'health') IS NOT NULL
            GROUP BY health
            ORDER BY cnt DESC
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        labels = [r[0] for r in rows] if rows else []
        series = [r[1] for r in rows] if rows else []
        return jsonify({"labels": labels, "series": series}), 200
    except Exception as e:
        logging.exception("Error in health_distribution")
        return jsonify({"labels": [], "series": [], "error": str(e)}), 500

@token_required
@app.route("/breed-distribution", methods=["GET"])
def breed_distribution(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT bovine->> 'breed' AS breed, COUNT(*) AS cnt
            FROM submissions, jsonb_array_elements(COALESCE(bovines::jsonb, '[]'::jsonb)) AS bovine
            WHERE (bovine->> 'breed') IS NOT NULL
            AND submissions.user_id = %s
            GROUP BY breed
            ORDER BY cnt DESC
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        labels = [r[0] for r in rows] if rows else []
        series = [r[1] for r in rows] if rows else []
        return jsonify({"labels": labels, "series": series}), 200
    except Exception as e:
        logging.exception("Error in breed_distribution")
        return jsonify({"labels": [], "series": [], "error": str(e)}), 500

@token_required
@app.route("/water-intake", methods=["GET"])
def water_distribution(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(user_id)
        cur.execute("""
            SELECT
                SUM(CASE WHEN water_intake IS NOT NULL AND water_intake < 20 THEN 1 ELSE 0 END) AS low,
                SUM(CASE WHEN water_intake BETWEEN 20 AND 40 THEN 1 ELSE 0 END) AS medium,
                SUM(CASE WHEN water_intake IS NOT NULL AND water_intake > 40 THEN 1 ELSE 0 END) AS high
            FROM submissions
        """, (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        low, med, high = (row[0] or 0, row[1] or 0, row[2] or 0) if row else (0, 0, 0)
        labels = ["Low", "Medium", "High"]
        series = [low, med, high]
        return jsonify({"labels": labels, "series": series}), 200
    except Exception as e:
        logging.exception("Error in water_distribution")
        return jsonify({"labels": ["Low", "Medium", "High"], "series": [0, 0, 0], "error": str(e)}), 500


# -------------------------
# Global error handler (single)
# -------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    logging.exception("Internal server error")
    return jsonify({
        "error": "Internal server error",
        "detail": str(e)
    }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
