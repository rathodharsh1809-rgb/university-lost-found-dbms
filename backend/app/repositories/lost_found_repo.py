"""
Data Access Layer (Repository)
Contains ALL SQL operations (INSERT, SELECT, UPDATE, JOIN).
Completely isolated from the UI and Presentation layer.
"""

from typing import List, Dict, Any, Optional
from backend.app.utils.db import get_db_connection


class LostFoundRepository:
    """Encapsulates SQL queries for the Lost & Found database."""

    # -------------------------------------------------------------------------
    # SELECT Queries
    # -------------------------------------------------------------------------
    @staticmethod
    def get_available_found_items() -> List[Dict[str, Any]]:
        """SELECT: Returns all available found items for browsing."""
        with get_db_connection() as conn:
            rows = conn.execute("""
                SELECT found_item_id, item_name, description, found_location, found_date, status, created_at
                FROM found_items
                WHERE status = 'AVAILABLE'
                ORDER BY found_item_id DESC;
            """).fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_found_item_by_id(found_item_id: int) -> Optional[Dict[str, Any]]:
        """SELECT: Returns a single found item record by ID."""
        with get_db_connection() as conn:
            row = conn.execute("""
                SELECT found_item_id, item_name, description, found_location, found_date, status, created_at
                FROM found_items
                WHERE found_item_id = ?;
            """, (found_item_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_lost_items_by_user(user_id: int) -> List[Dict[str, Any]]:
        """SELECT: Returns all lost items reported by a specific user."""
        with get_db_connection() as conn:
            rows = conn.execute("""
                SELECT lost_item_id, user_id, item_name, category, description, lost_location, lost_date, status, created_at
                FROM lost_items
                WHERE user_id = ?
                ORDER BY lost_item_id DESC;
            """, (user_id,)).fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_lost_item_by_id(lost_item_id: int) -> Optional[Dict[str, Any]]:
        """SELECT: Returns a single lost item record by ID."""
        with get_db_connection() as conn:
            row = conn.execute("""
                SELECT lost_item_id, user_id, item_name, category, description, lost_location, lost_date, status, created_at
                FROM lost_items
                WHERE lost_item_id = ?;
            """, (lost_item_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_all_lost_reports_with_user() -> List[Dict[str, Any]]:
        """
        JOIN Query: Returns all lost items joined with user details.
        Demonstrates relational DBMS JOIN between users and lost_items.
        """
        with get_db_connection() as conn:
            rows = conn.execute("""
                SELECT 
                    l.lost_item_id,
                    l.item_name,
                    l.category,
                    l.description,
                    l.lost_location,
                    l.lost_date,
                    l.status,
                    l.created_at,
                    u.user_id,
                    u.name AS student_name,
                    u.email AS student_email,
                    u.role AS user_role
                FROM lost_items l
                JOIN users u ON l.user_id = u.user_id
                ORDER BY l.lost_item_id DESC;
            """).fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_notifications_for_user(user_id: int) -> List[Dict[str, Any]]:
        """SELECT: Returns all notifications for a specific user."""
        with get_db_connection() as conn:
            rows = conn.execute("""
                SELECT notification_id, user_id, message, is_read, created_at
                FROM notifications
                WHERE user_id = ?
                ORDER BY notification_id DESC;
            """, (user_id,)).fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_unread_notification_count(user_id: int) -> int:
        """SELECT COUNT: Returns count of unread notifications for student."""
        with get_db_connection() as conn:
            count = conn.execute("""
                SELECT COUNT(*) FROM notifications
                WHERE user_id = ? AND is_read = 0;
            """, (user_id,)).fetchone()[0]
            return int(count)

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """SELECT: Returns user record by ID."""
        with get_db_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,)).fetchone()
            return dict(row) if row else None

    # -------------------------------------------------------------------------
    # INSERT Queries
    # -------------------------------------------------------------------------
    @staticmethod
    def insert_lost_item(user_id: int, item_name: str, category: str, 
                         description: str, lost_location: str, lost_date: str) -> int:
        """
        INSERT: Adds a new lost item record with default status 'SEARCHING'.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO lost_items (user_id, item_name, category, description, lost_location, lost_date, status)
                VALUES (?, ?, ?, ?, ?, ?, 'SEARCHING');
            """, (user_id, item_name, category, description, lost_location, lost_date))
            return cursor.lastrowid

    @staticmethod
    def insert_notification(user_id: int, message: str) -> int:
        """
        INSERT: Dispatches a new notification to a user.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notifications (user_id, message, is_read)
                VALUES (?, ?, 0);
            """, (user_id, message))
            return cursor.lastrowid

    # -------------------------------------------------------------------------
    # DELETE Queries
    # -------------------------------------------------------------------------
    @staticmethod
    def delete_found_item(found_item_id: int) -> bool:
        """
        DELETE: Permanently removes a found item record from SQLite.
        Uses parameterized SQL query.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM found_items
                WHERE found_item_id = ?;
            """, (found_item_id,))
            return cursor.rowcount > 0

    # -------------------------------------------------------------------------
    # UPDATE Queries
    # -------------------------------------------------------------------------
    @staticmethod
    def update_lost_item_status(lost_item_id: int, status: str) -> bool:
        """
        UPDATE: Updates the status of a lost item (e.g. from 'SEARCHING' to 'FOUND').
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE lost_items
                SET status = ?
                WHERE lost_item_id = ?;
            """, (status, lost_item_id))
            return cursor.rowcount > 0

    @staticmethod
    def mark_notifications_as_read(user_id: int) -> None:
        """UPDATE: Marks all notifications for a user as read."""
        with get_db_connection() as conn:
            conn.execute("""
                UPDATE notifications
                SET is_read = 1
                WHERE user_id = ?;
            """, (user_id,))
