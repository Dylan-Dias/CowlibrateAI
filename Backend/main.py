from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import bcrypt
import jwt
import datetime
from flask_mail import Mail, Message


app = Flask(__name__)
CORS(app)

JWT_SECRET = "800f985c9c3224c035a901222c801cd6"

def get_db_connection():
    return psycopg2.connect(
        dbname="CowlibrateAI",
        user="postgres",
        password="root",
        host="localhost"
    )

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")  # default role if not provided

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (username, email, hashed.decode('utf-8'), role)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logout", methods=["POST"])
def logout():
    # If you wanted server-side token invalidation, you'd handle it here
    return jsonify({"message": "Logout successful"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, role FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    user_id, password_hash, role = user

    if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        token = jwt.encode(
            {"user_id": user_id, "role": role, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            JWT_SECRET,
            algorithm="HS256"
        )
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user_id": user_id,
            "role": role,
            "token": token
        })
    else:
        return jsonify({"error": "Invalid username or password"}), 401

app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config["MAIL_PORT"] = 587
app.config['MAIL_USERNAME'] = 'smtp@mailtrap.io'
app.config['MAIL_PASSWORD'] = '1f8d6cfb234bb2a408d1c13001902a58'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False 

mail = Mail(app)

@app.route("/send-email")
def send_email():
    msg = Message(
        subject="Hello from Mailtrap",
        sender="dylandias960@yahoo.com",
        recipients=['ddias@drew.edu'],
        body="This is a test email sent via Mailtrap"
    )
    mail.send(msg)
    return "Email Sent!"
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
