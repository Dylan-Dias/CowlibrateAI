# Backend/wsgi.py
from .submissions import create_app  # relative import
app = create_app()
