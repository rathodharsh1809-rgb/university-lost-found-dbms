"""
Backend Configuration Module
Centralizes project paths, database file locations, and Flask configuration.
"""

import os

# Project root is two levels up from backend/config.py (i.e. MU2/)
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))

# Central Database Paths
DATABASE_DIR = os.path.join(PROJECT_ROOT, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "lost_and_found.db")
SCHEMA_PATH = os.path.join(DATABASE_DIR, "schema.sql")
SEED_PATH = os.path.join(DATABASE_DIR, "seed.sql")
QUERIES_PATH = os.path.join(DATABASE_DIR, "queries.sql")

# Frontend Asset Paths
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

# Flask Settings & Security
SECRET_KEY = os.environ.get("SECRET_KEY", "university-lost-found-dbms-academic-key")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin@123")
DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 5000))

