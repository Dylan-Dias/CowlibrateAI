import os
import json
import logging
import datetime
from functools import wraps
from dotenv import load_dotenv

import bcrypt
import jwt
import psycopg
from psycopg import rows
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Message
from flask import url_for
from itsdangerous import URLSafeTimedSerializer


# -------------------------
# Load env variables
# -------------------------
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

if not JWT_SECRET or not DATABASE_URL:
    raise RuntimeError("Missing required environment variables (JWT_SECRET, DATABASE_URL)")

# -------------------------
# Flask setup
# -------------------------
app = Flask(__name__)
FRONTEND_URLS = os.environ.get("FRONTEND_URLS", "")
origins = FRONTEND_URLS.split(",") if FRONTEND_URLS else []
CORS(app, resources={r"/*": {"origins": origins}})
# Logging
logging.basicConfig(level=logging.INFO)

# Mail (optional)
app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER")
)
mail = Mail(app)

limiter = Limiter(
    key_func=get_remote_address,  # specify key_func explicitly
    app=app
)

# -------------------------
# Database helper
# -------------------------
def get_db_connection():
        return psycopg.connect(DATABASE_URL, row_factory=rows.dict_row)

# -------------------------
# JWT auth decorator
# -------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(user_id, *args, **kwargs)

    return decorated


# Token Helper Function 

SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
if not SECURITY_PASSWORD_SALT:
    raise RuntimeError("Missing SECURITY_PASSWORD_SALT in .env")

def generate_reset_token(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow()+ datetime.timedelta(hours=1)

    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def confirm_reset_token(token):
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return data["email"]
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False 

def send_reset_email(user_email):
    token = generate_reset_token(user_email)
    reset_url = url_for("reset_password", token=token, _external=True)
    msg = Message(
        subject="Password Reset Request",
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user_email],
        body=f"Hi,\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you didn't request this, ignore this email.\n\nThanks!"
    )
    mail.send(msg)
# -------------------------
# Auth Routes
# -------------------------
@app.route("/")
def index():
    return "CowlibrateAI backend is running", 200

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username, email, password = data.get("username"), data.get("email"), data.get("password")
    role = data.get("role", "user")

    if not all([username, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (username, email, password_hash, role)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (username, email, hashed_password, role))
            user_id = cur.fetchone()["id"]

        token = jwt.encode({
            "user_id": user_id,
            "role": role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, JWT_SECRET, algorithm="HS256")

        return jsonify({
            "success": True,
            "message": "User Registered successfully",
            "token": token,
            "user": {"id": user_id, "username": username, "email": email, "role": role}
        }), 201

    except Exception as e:
        logging.exception("Username or Email already exists")
        return jsonify({
            "error": "Username or Email already exists",
            "code": "USER_EXISTS",
            "action": "LOGIN"
        }), 409 


@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json() or {}
    username, password = data.get("username"), data.get("password")

    if not all([username, password]):
        return jsonify({"error": "Missing fields"}), 400

    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT id, password_hash, role FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

        if not user:
            return jsonify({"error": "Invalid username or password"}), 401

        password_hash = user["password_hash"]
        if bcrypt.checkpw(password.encode(), password_hash.encode()):
            token = jwt.encode({
                "user_id": user["id"],
                "role": user["role"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, JWT_SECRET, algorithm="HS256")

            return jsonify({
                "success": True,
                "message": "Login successful",
                "user_id": user["id"],
                "role": user["role"],
                "token": token
            })

        return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        logging.exception("Login error")
        return jsonify({"error": "To many Failed Attempts, please wait 5 minutes", "detail": str(e)}), 500

@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logout successful"}), 200

# Password Rest WHAT I AM CURRENTLY WORKING ON
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

        if not user:
            # Always return success message to avoid leaking info
            return jsonify({"message": "If that email exists, a reset link has been sent."})

        # Create token for password reset
        token = jwt.encode({
        "user_id": user["id"],
        "email": email,          # <-- add this
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, JWT_SECRET, algorithm="HS256")


        reset_link = f"https://cowlibrate.onrender.com/reset-password/{token}"

        # Send email
        msg = Message(
            subject="Password Reset for CowlibrateAI",
            recipients=[email],
            body=f"Click this link to reset your password: {reset_link}"
        )
        mail.send(msg)

        return jsonify({"message": "If that email exists, a reset link has been sent."})

    except Exception as e:
        logging.exception("Forgot password error")
        return jsonify({"error": "Failed to send reset email", "detail": str(e)}), 500
    
# Reset Password Endpoint 
@app.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    data = request.get_json() or {}
    new_password = data.get("password")
    if not new_password:
        return jsonify({"error": "Password is required"}), 400

    email = confirm_reset_token(token)
    if not email:
        return jsonify({"error": "Invalid or expired token"}), 400

    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_password, email))
            conn.commit()
        return jsonify({"message": "Password reset successfully"}), 200

    except Exception as e:
        logging.exception("Reset password failed")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    try:
        # Save to database
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                INSERT INTO contact_submissions (name, email, message, created_at)
                VALUES (%s, %s, %s, NOW())
            """, (name, email, message))
            conn.commit()

        return jsonify({"success": "Message recorded successfully!"}), 201
    except Exception as e:
        logging.exception("Contact form failed")
        return jsonify({"error": str(e)}), 500


# Routes for CRUD Database Buttons
# Get All Submissions 
@app.route("/api/submissions", methods=["GET"])
@token_required
def get_submissions(user_id):
    conn = get_db_connection()
    cur = conn.cursor()  # row_factory is already set in connection
    cur.execute("SELECT * FROM submissions WHERE user_id = %s", (user_id,))
    results = cur.fetchall()  # each row is a dict


    cur.execute(
        "SELECT id, bovines, feeds FROM submissions WHERE user_id = %s ORDER BY id DESC",
        (user_id,)
    )

    items = cur.fetchall()

    # Parse JSON fields
    for item in items:
        for field in ["bovines", "feeds"]:
            if field in item and isinstance(item[field], str):
                try:
                    item[field] = json.loads(item[field])
                except:
                    item[field] = []

    cur.close()
    conn.close()

    return jsonify(items), 200



# Get Single Submissions 
@app.route("/api/submissions/<int:item_id>", methods=["GET"])
@token_required
def get_submission(item_id):
    user_id = request.user["id"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM submissions WHERE id = %s AND user_id = %s",
        (item_id, user_id)
    )
    item = cur.fetchone()
    cur.close()
    conn.close()

    if not item:
        return jsonify({"error": "Not found"}), 404

    return jsonify(item), 200

# Create Submissions 
@app.route("/api/submissions", methods=["POST"])
@token_required
def create_submission(user_id):
    user_id = request.user["id"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO submissions (user_id) VALUES (%s) RETURNING *",
        (user_id,)
    )
    new_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_item), 201

# Update Submissions
@app.route("/api/submissions/<int:item_id>", methods=["PUT"])
@token_required
def update_submission(item_id):
    user_id = request.user["id"]

    # Since there are no editable fields right now,
    # we just check ownership.
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM submissions WHERE id = %s AND user_id = %s",
        (item_id, user_id)
    )
    item = cur.fetchone()

    if not item:
        cur.close()
        conn.close()
        return jsonify({"error": "Not found"}), 404

    # Placeholder update (no real fields)
    cur.execute(
        "UPDATE submissions SET user_id = %s WHERE id = %s RETURNING *",
        (user_id, item_id)
    )
    updated_item = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(updated_item), 200

# Delete Submissions
@app.route("/api/submissions/<int:item_id>", methods=["DELETE"])
@token_required
def delete_submission(item_id):
    user_id = request.user["id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM submissions WHERE id = %s AND user_id = %s RETURNING id",
        (item_id, user_id)
    )
    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        return jsonify({"error": "Not found"}), 404

    return jsonify({"message": "Deleted"}), 200

# -------------------------
# Optimization Routes
# -------------------------
@app.route("/api/optimize", methods=["POST"])
@token_required
def optimize(user_id):
    data = request.get_json() or {}
    bovines = data.get("bovines", [])
    if not bovines:
        return jsonify({"error": "bovines must be a non-empty list"}), 400

    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                INSERT INTO submissions (user_id, bovines, feeds, indoor_temp, outdoor_temp,
                    water_intake, budget, protein, butterfat, somatic_cell_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, created_at
            """, (
                user_id,
                json.dumps(bovines),
                json.dumps(data.get("feeds", [])),
                data.get("indoor_temp"),
                data.get("outdoor_temp"),
                data.get("water_intake"),
                data.get("budget"),
                data.get("protein"),
                data.get("butterfat"),
                data.get("somatic_cell_count")
            ))
            submission = cur.fetchone()

        # Optimization placeholder logic
        optimized = []
        for b in bovines:
            try:
                score = round(min(100, max(0, float(b.get("milk_yield", 0)) * 3 - float(b.get("age", 0)) * 0.5)))
            except Exception:
                score = 0
            optimized.append({**b, "score": score})

        # Save optimized cows
        with get_db_connection() as conn, conn.cursor() as cur:
            for cow in optimized:
                cur.execute("""
                    INSERT INTO selected_cows (submission_id, user_id, cow_id, age, breed,
                        health, milk_yield, lactation_stage, score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    submission["id"], user_id,
                    cow.get("id"), cow.get("age"), cow.get("breed"),
                    cow.get("health"), cow.get("milk_yield"),
                    cow.get("lactation_stage"), cow.get("score")
                ))

            cur.execute("""
                INSERT INTO optimization_results (submission_id, user_id, results)
                VALUES (%s, %s, %s)
            """, (submission["id"], user_id, json.dumps(optimized)))
            conn.commit()

        return jsonify({
            "message": "Optimization completed and saved",
            "submission_id": submission["id"],
            "timestamp": submission["created_at"],
            "results": optimized
        }), 201

    except Exception as e:
        logging.exception("Optimization failed")
        return jsonify({"error": "Optimization failed", "detail": str(e)}), 500

@app.route("/api/optimization-results", methods=["GET"])
@token_required
def optimization_results(user_id):
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT id FROM submissions WHERE user_id = %s
                ORDER BY created_at DESC LIMIT 1
            """, (user_id,))
            submission = cur.fetchone()
            if not submission:
                return jsonify({"results": []}), 200

            cur.execute("""
                SELECT cow_id, age, breed, health, milk_yield,
                    lactation_stage, score, created_at
                FROM selected_cows
                WHERE submission_id = %s
                ORDER BY score DESC, created_at ASC
            """, (submission["id"],))
            rows = cur.fetchall()
        return jsonify({"results": rows}), 200
    except Exception as e:
        logging.exception("Fetch results failed")
        return jsonify({"error": str(e)}), 500

# -------------------------
# Analytics / Chart Endpoints
# -------------------------
@app.route("/MilkYield-distribution", methods=["GET"])
@token_required
def milk_yield_distribution(user_id):
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    created_at::date AS day,
                    SUM((bovine->>'milk_yield')::numeric) AS total_yield
                FROM submissions,
                jsonb_array_elements(COALESCE(bovines::jsonb, '[]'::jsonb)) AS bovine
                WHERE bovine->>'type' = 'milk_yield'
                AND bovine ? 'milk_yield'
                AND date_part('year', created_at) = date_part('year', CURRENT_DATE)
                AND date_part('month', created_at) = date_part('month', CURRENT_DATE)
                GROUP BY day
                ORDER BY day;
            """)
            
            rows = cur.fetchall()

        return (
            jsonify({
                "labels": [r["day"].strftime("%Y-%m-%d") for r in rows],
                "series": [float(r["total_yield"]) for r in rows]
            }),
            200
        )

    except Exception as e:
        logging.exception("Error in milk_yield_distribution")
        return jsonify({"labels": [], "series": [], "error": str(e)}), 500

@app.route("/health-distribution", methods=["GET"])
@token_required
def health_distribution(user_id):
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT
                COALESCE(bovine->>'health', 'unknown') AS health,
                COUNT(*) AS cnt
                FROM submissions,
                jsonb_array_elements(COALESCE(bovines::jsonb, '[]'::jsonb)) AS bovine
                WHERE submissions.user_id = %s
                GROUP BY health
                ORDER BY cnt DESC;


            """, (user_id,))
            rows = cur.fetchall()
        return jsonify({"labels": [r["health"] for r in rows], "series": [r["cnt"] for r in rows]}), 200
    except Exception as e:
        logging.exception("Error in health_distribution")
        return jsonify({"labels": [], "series": [], "error": str(e)}), 500

@app.route("/breed-distribution", methods=["GET"])
@token_required
def breed_distribution(user_id):
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT bovine->> 'breed' AS breed, COUNT(*) AS cnt
                FROM submissions, jsonb_array_elements(COALESCE(bovines::jsonb, '[]'::jsonb)) AS bovine
                WHERE submissions.user_id = %s
                GROUP BY breed
                ORDER BY cnt DESC
            """, (user_id,))
            rows = cur.fetchall()
        return jsonify({"labels": [r["breed"] for r in rows], "series": [r["cnt"] for r in rows]}), 200
    except Exception as e:
        logging.exception("Error in breed_distribution")
        return jsonify({"labels": [], "series": [], "error": str(e)}), 500

# Water needs to get fixed
@app.route("/water-intake", methods=["GET"])
@token_required
def water_distribution(user_id):
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT
                    SUM(CASE WHEN water_intake < 20 THEN 1 ELSE 0 END) AS low,
                    SUM(CASE WHEN water_intake BETWEEN 20 AND 40 THEN 1 ELSE 0 END) AS medium,
                    SUM(CASE WHEN water_intake > 40 THEN 1 ELSE 0 END) AS high
                FROM submissions
                WHERE user_id = %s
            """, (user_id,))
            row = cur.fetchone()
        labels = ["Low", "Medium", "High"]
        series = [row["low"] or 0, row["medium"] or 0, row["high"] or 0] if row else [0, 0, 0]
        return jsonify({"labels": labels, "series": series}), 200
    except Exception as e:
        logging.exception("Error in water_distribution")
        return jsonify({"labels": ["Low", "Medium", "High"], "series": [0, 0, 0], "error": str(e)}), 500

# -------------------------
# Global Error Handler
# -------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    logging.exception("Unhandled Exception")
    return jsonify({"error": "Internal server error", "detail": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
