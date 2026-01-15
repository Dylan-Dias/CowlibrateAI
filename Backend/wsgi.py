# Backend/wsgi.py
from .submissions import create_app  # relative import from Backend package

app = create_app()
