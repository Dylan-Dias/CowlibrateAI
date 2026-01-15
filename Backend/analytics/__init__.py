# analytics/__init__.py

from flask import Blueprint

# Create blueprint
analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")

# Import routes so they get registered with the blueprint
from . import routes
