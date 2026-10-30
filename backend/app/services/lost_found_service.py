"""
Application / Business Logic Layer
Orchestrates business workflows, validates input, and directs repository operations.
Completely decoupled from presentation templates and database connection drivers.
"""

from typing import List, Dict, Any, Tuple
from backend.app.repositories.lost_found_repo import LostFoundRepository


class LostFoundService:
    """Service providing business logic for Lost & Found portal."""

    DEMO_STUDENT_ID = 1  # Rahul (Student)
    DEMO_ADMIN_ID = 2    # Lost & Found Department (Admin)

    @classmethod
    def get_browse_items(cls) -> List[Dict[str, Any]]:
        """Retrieves list of found items currently available in the department."""
        return LostFoundRepository.get_available_found_items()

    @classmethod
    def remove_found_item(cls, found_item_id: int) -> Tuple[bool, str]:
        """
        Removes a found item from SQLite database.
        Validates item existence and that status is 'AVAILABLE'.
        """
        item = LostFoundRepository.get_found_item_by_id(found_item_id)
        if not item:
            return False, "Item not found."

        if item.get("status") != "AVAILABLE":
            return False, "Only available items can be removed."

        deleted = LostFoundRepository.delete_found_item(found_item_id)
        if deleted:
            return True, f"Found item '{item['item_name']}' was removed successfully."
        return False, "Failed to remove the found item."

    @classmethod
    def report_lost_item(cls, user_id: int, item_name: str, category: str,
                         description: str, lost_location: str, lost_date: str) -> Tuple[bool, str, int]:
        """
        Validates input and triggers SQL INSERT into lost_items.
        """
        if not item_name or not item_name.strip():
            return False, "Item name is required.", 0
        if not lost_location or not lost_location.strip():
            return False, "Lost location is required.", 0
        if not lost_date or not lost_date.strip():
            return False, "Lost date is required.", 0

        # Execute insertion via repository
        new_id = LostFoundRepository.insert_lost_item(
            user_id=user_id,
            item_name=item_name.strip(),
            category=category.strip() if category else "General",
            description=description.strip() if description else "",
            lost_location=lost_location.strip(),
            lost_date=lost_date.strip()
        )
        return True, f"Lost item report for '{item_name}' registered successfully.", new_id

    @classmethod
    def get_student_reports(cls, user_id: int) -> List[Dict[str, Any]]:
        """Returns all lost items reported by student."""
        return LostFoundRepository.get_lost_items_by_user(user_id)

    @classmethod
    def get_admin_reports(cls) -> List[Dict[str, Any]]:
        """Returns all lost reports with student details using relational JOIN."""
        return LostFoundRepository.get_all_lost_reports_with_user()

    @classmethod
    def mark_lost_item_as_found(cls, lost_item_id: int) -> Tuple[bool, str]:
        """
        Business transaction:
        1. Updates status of lost item to 'FOUND'
        2. Creates an automated notification for the student
        """
        item = LostFoundRepository.get_lost_item_by_id(lost_item_id)
        if not item:
            return False, "Lost item record not found."

        # Update status
        updated = LostFoundRepository.update_lost_item_status(lost_item_id, "FOUND")
        if not updated:
            return False, "Failed to update item status."

        # Dispatch notification to student
        notification_msg = f"Your {item['item_name']} has been found. Please visit the Lost & Found Department."
        LostFoundRepository.insert_notification(item["user_id"], notification_msg)

        return True, f"Item #{lost_item_id} ('{item['item_name']}') marked as FOUND. Notification sent to student."

    @classmethod
    def get_notifications(cls, user_id: int) -> List[Dict[str, Any]]:
        """Returns student notifications and marks them as read."""
        notifications = LostFoundRepository.get_notifications_for_user(user_id)
        LostFoundRepository.mark_notifications_as_read(user_id)
        return notifications

    @classmethod
    def get_unread_count(cls, user_id: int) -> int:
        """Returns unread notification badge count."""
        return LostFoundRepository.get_unread_notification_count(user_id)

    @classmethod
    def get_dashboard_data(cls) -> Dict[str, Any]:
        """
        Aggregates all system metrics, registries, and physical DBMS metadata
        for the master executive dashboard.
        """
        from backend.app.utils.db import get_internal_metadata
        
        aggregates = LostFoundRepository.get_dashboard_aggregates()
        lost_items = LostFoundRepository.get_all_lost_reports_with_user()
        found_items = LostFoundRepository.get_all_found_items()
        users = LostFoundRepository.get_all_users_with_stats()
        notifications = LostFoundRepository.get_all_notifications_with_users()
        db_metadata = get_internal_metadata()

        return {
            "aggregates": aggregates,
            "lost_items": lost_items,
            "found_items": found_items,
            "users": users,
            "notifications": notifications,
            "db_metadata": db_metadata
        }

