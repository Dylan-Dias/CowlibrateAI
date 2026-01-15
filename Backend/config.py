import os 
from dotenv import load_dotenv

load_dotenv()

class Config: 
    SECRET_KEY = os.getenv("JWT_SECRET")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    FRONTEND_URLS = os.getenv("FRONTEND_URLS", "").split(",")

    