from submissions import create_app
from flask_cors import CORS

app = create_app()

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://cowlibrate.com",
                "https://cowlibrate.pt"
            ]
        }
    },
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization"]
)

@app.route("/")
def index():
    return "CowlibrateAI backend is running", 200

if __name__ == "__main__":
    app.run()
