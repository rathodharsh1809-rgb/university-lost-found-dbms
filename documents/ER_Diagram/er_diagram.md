# Entity-Relationship (ER) Diagram

## Conceptual Relational Model

```mermaid
erDiagram
    USERS ||--o{ LOST_ITEMS : reports
    USERS ||--o{ NOTIFICATIONS : receives

    USERS {
        int user_id PK
        string name
        string email UK
        string role "CHECK: student, faculty, admin"
    }

    LOST_ITEMS {
        int lost_item_id PK
        int user_id FK
        string item_name
        string category
        string description
        string lost_location
        string lost_date
        string status "DEFAULT: SEARCHING"
        timestamp created_at
    }

    FOUND_ITEMS {
        int found_item_id PK
        string item_name
        string description
        string found_location
        string found_date
        string status "DEFAULT: AVAILABLE"
        timestamp created_at
    }

    NOTIFICATIONS {
        int notification_id PK
        int user_id FK
        string message
        int is_read "CHECK: 0, 1"
        timestamp created_at
    }
```

---

## Cardinality & Relationships

1. **`USERS 1 ──── N LOST_ITEMS`**
   - **One user** can report **zero or many** lost items.
   - **Each lost item** belongs to **exactly one** user.
   - **Foreign Key**: `lost_items.user_id` &rarr; `users.user_id` (`ON DELETE CASCADE`).

2. **`USERS 1 ──── N NOTIFICATIONS`**
   - **One user** can receive **zero or many** automated notifications.
   - **Each notification** is addressed to **exactly one** user.
   - **Foreign Key**: `notifications.user_id` &rarr; `users.user_id` (`ON DELETE CASCADE`).

3. **`FOUND_ITEMS`**
   - Standalone campus inventory entity tracking items turned in to the Lost & Found desk.
