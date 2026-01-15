from flask import Flask
from flask_cors import CORS
from submissions import create_app

app = create_app()

# Allow requests from your frontend
CORS(app, origins=["https://cowlibrate.com"], supports_credentials=True)

if __name__ == "__main__":
    app.run()
