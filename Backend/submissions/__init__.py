from flask import Flask
from Backend.extensions import mail, cors, limiter
from Backend.auth.routes import auth_bp  # if needed
# any other imports that used relative paths

# submissions/__init__.py
from Backend.submissions.routes import submissions_bp

from Backend.analytics.routes import analytics_bp


def create_app():
    """Factory function to create Flask app"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("Backend.config.Config")

    # Initialize extensions
    mail.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(submissions_bp, url_prefix="/api/submissions")
    # app.register_blueprint(optimization_bp, url_prefix="/api/submissions/optimization")
    app.register_blueprint(analytics_bp)

    return app
