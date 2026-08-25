"""
Domain Models representing Conceptual Entities
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: int
    name: str
    email: str
    role: str


@dataclass
class LostItem:
    lost_item_id: int
    user_id: int
    item_name: str
    category: Optional[str]
    description: Optional[str]
    lost_location: Optional[str]
    lost_date: Optional[str]
    status: str = "SEARCHING"
    created_at: Optional[str] = None


@dataclass
class FoundItem:
    found_item_id: int
    item_name: str
    description: Optional[str]
    found_location: Optional[str]
    found_date: Optional[str]
    status: str = "AVAILABLE"
    created_at: Optional[str] = None


@dataclass
class Notification:
    notification_id: int
    user_id: int
    message: str
    is_read: int = 0
    created_at: Optional[str] = None
