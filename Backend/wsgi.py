# wsgi.py
from submissions import create_app
from flask_cors import CORS
from flask import Flask

# Create the Flask app using your factory
app = create_app()

CORS(
    app,
    origins=["https://cowlibrate.com", "https://cowlibrate.pt"],
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

# Optional: add a root route to prevent 404
@app.route("/")
def index():
    return "CowlibrateAI backend is running", 200

if __name__ == "__main__":
    # Only used when running locally
    app.run(debug=True)
