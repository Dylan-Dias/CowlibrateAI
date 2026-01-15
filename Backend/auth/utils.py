# auth/utils.py
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from ..config import Config  # your global config file with SECRET_KEY
from ..extensions import mail  # Flask-Mail
from flask_mail import Message

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
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(user_id, *args, **kwargs)
    return decorated

def generate_reset_token(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def confirm_reset_token(token):
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return data["email"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False

def send_reset_email(user_email):
    token = generate_reset_token(user_email)
    reset_link = f"https://cowlibrate.onrender.com/reset-password/{token}"
    msg = Message(
        subject="Password Reset Request",
        sender="no-reply@cowlibrate.com",
        recipients=[user_email],
        body=f"Click the link to reset your password: {reset_link}"
    )
    mail.send(msg)
    return jsonify({"message": "If that email exists, a reset link has been sent."})
