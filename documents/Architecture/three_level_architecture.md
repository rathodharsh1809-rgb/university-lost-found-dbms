# DBMS Three-Level Architecture Specification

The **ANSI/SPARC Three-Level Architecture** is implemented in the University Lost & Found Department system to separate user views, logical structure, and physical database files.

```
+--------------------------------------------------------------------------------------------------+
|                                    EXTERNAL LEVEL (View Level)                                   |
|   • Student View (Browse, Report Lost Item, My Reports, Notifications)                           |
|   • Admin View (Campus-wide Lost Reports, Student details via JOIN, Mark as Found action)        |
|   • Principle: Each user role interacts only with data and actions relevant to their permission. |
+--------------------------------------------------------------------------------------------------+
                                                 ▲
                                                 │ (Logical Data Independence)
                                                 ▼
+--------------------------------------------------------------------------------------------------+
|                                  CONCEPTUAL LEVEL (Logical Level)                                |
|   • Entities: users, lost_items, found_items, notifications                                      |
|   • Relational Schema, Primary Keys, Foreign Keys (users 1 ─── N lost_items), Constraints        |
+--------------------------------------------------------------------------------------------------+
                                                 ▲
                                                 │ (Physical Data Independence)
                                                 ▼
+--------------------------------------------------------------------------------------------------+
|                                   INTERNAL LEVEL (Physical Level)                                |
|   • SQLite file: database/lost_and_found.db                                                      |
|   • Managed physical disk pages, B-Tree table structures, and record allocation by SQLite engine |
+--------------------------------------------------------------------------------------------------+
```

---

## 1. External Level (View Level)
The External Level represents individual user perspectives:
- **Student View**:
  - Browse public found items.
  - Submit lost reports.
  - View personal submitted items and notifications.
- **Admin View (Password Protected)**:
  - Accessible only with administrator authentication (`admin@123`).
  - View all campus lost reports combined with student contact info via SQL JOIN.
  - Update status (`SEARCHING` → `FOUND`) and trigger automated notifications.
  - Session-based access control (`@admin_required`) with explicit logout.

---

## 2. Conceptual Level (Logical Level)
The Conceptual Level represents the global logical design of the entire database:
- **`users`**: `user_id` (PK), `name`, `email` (UNIQUE), `role` (CHECK constraint).
- **`lost_items`**: `lost_item_id` (PK), `user_id` (FK), `item_name`, `category`, `lost_location`, `lost_date`, `status`.
- **`found_items`**: `found_item_id` (PK), `item_name`, `description`, `found_location`, `found_date`, `status`.
- **`notifications`**: `notification_id` (PK), `user_id` (FK), `message`, `is_read`, `created_at`.

---

## 3. Internal Level (Physical Level)
The Internal Level describes the physical storage representation on disk:
- **Database Engine**: SQLite 3 file-based engine.
- **Database File**: `database/lost_and_found.db`.
- **Storage Management**: Managed automatically by SQLite using B-Tree indexing, 4096-byte pages, journal rollback, and UTF-8 encoding.
