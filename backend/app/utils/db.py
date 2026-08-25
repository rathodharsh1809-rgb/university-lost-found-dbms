"""
Backend Data Utility: SQLite Connection & Initialization Manager
Enforces foreign keys, manages connection lifecycle, and bootstraps schema & seeds.
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import Generator, Dict, Any
from backend.config import DATABASE_PATH, SCHEMA_PATH, SEED_PATH, DATABASE_DIR


def get_db_path() -> str:
    """Returns absolute path of the SQLite database file."""
    return DATABASE_PATH


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager providing a managed SQLite connection.
    Enforces foreign keys, busy timeout, and WAL mode for concurrent access with DB Browser.
    """
    os.makedirs(DATABASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 5000;")
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_database(force_reseed: bool = False) -> None:
    """
    Initializes database tables and seeds demo data if database does not exist.
    """
    os.makedirs(DATABASE_DIR, exist_ok=True)
    db_exists = os.path.exists(DATABASE_PATH)

    if not db_exists or force_reseed:
        conn = sqlite3.connect(DATABASE_PATH, timeout=20.0)
        try:
            conn.execute("PRAGMA foreign_keys = OFF;")
            if os.path.exists(SCHEMA_PATH):
                with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                    conn.executescript(f.read())
            if os.path.exists(SEED_PATH):
                with open(SEED_PATH, "r", encoding="utf-8") as f:
                    conn.executescript(f.read())
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.commit()
        finally:
            conn.close()


def get_internal_metadata() -> Dict[str, Any]:
    """
    Returns Physical/Internal level information for database inspection.
    """
    file_size_bytes = os.path.getsize(DATABASE_PATH) if os.path.exists(DATABASE_PATH) else 0
    file_size_kb = round(file_size_bytes / 1024, 2)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        page_size = cursor.execute("PRAGMA page_size;").fetchone()[0]
        page_count = cursor.execute("PRAGMA page_count;").fetchone()[0]
        encoding = cursor.execute("PRAGMA encoding;").fetchone()[0]
        journal_mode = cursor.execute("PRAGMA journal_mode;").fetchone()[0]

        tables = cursor.execute("""
            SELECT name, sql FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%';
        """).fetchall()

        table_info = []
        for t in tables:
            count = cursor.execute(f"SELECT COUNT(*) FROM {t['name']}").fetchone()[0]
            table_info.append({
                "name": t["name"],
                "row_count": count,
                "sql": t["sql"]
            })

    return {
        "file_name": "lost_and_found.db",
        "relative_path": "database/lost_and_found.db",
        "absolute_path": DATABASE_PATH,
        "file_size_kb": file_size_kb,
        "file_size_bytes": file_size_bytes,
        "page_size": page_size,
        "page_count": page_count,
        "encoding": encoding,
        "journal_mode": journal_mode,
        "tables": table_info
    }
