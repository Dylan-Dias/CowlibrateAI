# wsgi.py
from submissions import create_app
from flask_cors import CORS

# Create the Flask app using your factory
app = create_app()

# Enable CORS for both frontends
CORS(app, origins=["https://cowlibrate.com", "https://cowlibrate.pt"], supports_credentials=True)

# Optional: add a root route to prevent 404
@app.route("/")
def index():
    return "CowlibrateAI backend is running", 200

if __name__ == "__main__":
    # Only used when running locally
    app.run(debug=True)
