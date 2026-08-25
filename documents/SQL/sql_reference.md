# SQL Operations Reference

All SQL operations are encapsulated in `backend/app/repositories/lost_found_repo.py` and saved in `database/queries.sql`.

---

## 1. DDL (Data Definition Language)

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'faculty', 'admin'))
);

CREATE TABLE lost_items (
    lost_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    category TEXT,
    description TEXT,
    lost_location TEXT,
    lost_date TEXT,
    status TEXT NOT NULL DEFAULT 'SEARCHING' CHECK(status IN ('SEARCHING', 'FOUND', 'COLLECTED')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE found_items (
    found_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    description TEXT,
    found_location TEXT,
    found_date TEXT,
    status TEXT DEFAULT 'AVAILABLE' CHECK(status IN ('AVAILABLE', 'CLAIMED', 'DISPOSED')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

## 2. DML (Data Manipulation Language)

### A. INSERT Operations
1. **Student Reports Lost Item**:
```sql
INSERT INTO lost_items (
    user_id, item_name, category, description, lost_location, lost_date, status
) VALUES (
    1, 'DBMS Book', 'Books & Stationery', 'Blue cover textbook', 'Computer Lab 3', '25-08-2026', 'SEARCHING'
);
```

2. **Admin Adds Found Item**:
```sql
INSERT INTO found_items (
    item_name, description, found_location, found_date, status
) VALUES (
    'Scientific Calculator TI-84', 'Blue casing with sticker', 'Math Block Hall 2', '25-08-2026', 'AVAILABLE'
);
```

### B. SELECT Operations
1. **Browse Available Found Items (Database-driven)**:
```sql
SELECT found_item_id, item_name, description, found_location, found_date, status, created_at
FROM found_items
WHERE status = 'AVAILABLE'
ORDER BY found_item_id DESC;
```

2. **Student's Lost Reports**:
```sql
SELECT lost_item_id, item_name, category, description, lost_location, lost_date, status, created_at
FROM lost_items
WHERE user_id = 1
ORDER BY lost_item_id DESC;
```

### C. DELETE Operation (User Self-Recovery with Ownership Check)
```sql
DELETE FROM lost_items
WHERE lost_item_id = 1
  AND user_id = 1;
```

### D. Relational JOIN Query (Admin Overview)
```sql
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
```

### E. UPDATE & Notification Workflow (Mark as Found)
```sql
-- 1. Update status
UPDATE lost_items
SET status = 'FOUND'
WHERE lost_item_id = 1;

-- 2. Dispatch notification
INSERT INTO notifications (user_id, message, is_read)
VALUES (1, 'Your DBMS Book has been found. Please visit the Lost & Found Department.', 0);
```
