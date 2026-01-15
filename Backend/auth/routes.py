import bcrypt
import jwt
import datetime
import logging
from flask import Blueprint, request, jsonify
from flask_mail import Message
from database import get_db_connection
from . import auth_bp  # blueprint from __init__.py
from utils import token_required, generate_reset_token, confirm_reset_token, send_reset_email
from extensions import mail, limiter  # assuming you have these set up globally
from utils import JWT_SECRET


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
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
        }, generate_reset_token.JWT_SECRET, algorithm="HS256")

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


@auth_bp.route("/login", methods=["POST", "OPTIONS"])
@limiter.limit("5 per minute")
def login():
    if request.method == "OPTIONS":
        return "", 200
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
            }, generate_reset_token.JWT_SECRET, algorithm="HS256")

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
        return jsonify({"error": "Too many Failed Attempts, please wait 5 minutes", "detail": str(e)}), 500


@auth_bp.route("/forgot-password", methods=["POST"])
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
            return jsonify({"message": "If that email exists, a reset link has been sent."})

        token = generate_reset_token(email)
        reset_link = f"https://cowlibrate.onrender.com/reset-password/{token}"

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


@auth_bp.route("/reset-password/<token>", methods=["POST"])
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