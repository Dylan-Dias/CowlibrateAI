from flask import Blueprint

from .routes import submissions_bp  # your routes for CRUD + optimize

# Optional: if you have more blueprints inside submissions
# from .optimization.routes import optimization_bp

__all__ = ["submissions_bp"]  # so other parts can import this easily
