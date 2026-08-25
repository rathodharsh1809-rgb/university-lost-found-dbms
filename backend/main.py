"""
University Lost & Found Department - Backend Application Entry Point
Initializes SQLite database and serves Flask application with decoupled frontend templates.
"""

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask
from backend.config import TEMPLATES_DIR, STATIC_DIR, SECRET_KEY, HOST, PORT, DEBUG, DATABASE_PATH
from backend.app.utils.db import initialize_database
from backend.app.routes.lost_found_routes import routes_bp


def create_app() -> Flask:
    """Application factory for Flask backend."""
    # Ensure physical database is initialized
    initialize_database()

    app = Flask(
        __name__,
        template_folder=TEMPLATES_DIR,
        static_folder=STATIC_DIR
    )
    app.config["SECRET_KEY"] = SECRET_KEY

    # Register Backend Routes Blueprint
    app.register_blueprint(routes_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    print("=" * 70)
    print(" UNIVERSITY LOST & FOUND DEPARTMENT - BACKEND SERVER")
    print("=" * 70)
    print(f" > Physical Database: {DATABASE_PATH}")
    print(" > Architecture: Frontend -> Backend Routes -> Services -> Repositories -> SQLite")
    print(f" > Live Server: http://{HOST}:{PORT}")
    print("=" * 70)
    app.run(host=HOST, port=PORT, debug=DEBUG)
