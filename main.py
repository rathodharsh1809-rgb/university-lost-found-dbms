"""
University Lost & Found Department - Root Application Launcher
Delegates to backend.main application factory.
"""

import sys
import os

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.main import create_app
from backend.config import HOST, PORT, DEBUG, DATABASE_PATH

if __name__ == "__main__":
    app = create_app()
    print("=" * 70)
    print(" UNIVERSITY LOST & FOUND DEPARTMENT - ACADEMIC DBMS MINI PROJECT")
    print("=" * 70)
    print(f" > Physical Database: {DATABASE_PATH}")
    print(" > Architecture: Frontend -> Backend -> Services -> Repositories -> SQLite")
    print(f" > Live Server: http://{HOST}:{PORT}")
    print("=" * 70)
    app.run(host=HOST, port=PORT, debug=DEBUG)
