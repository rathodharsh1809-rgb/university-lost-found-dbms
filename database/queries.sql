-- ============================================================================
-- UNIVERSITY LOST & FOUND DEPARTMENT - SQL QUERIES REFERENCE
-- Demonstrates DDL, DML (INSERT, SELECT, UPDATE, DELETE), and Relational JOINs
-- Compatible with DB Browser for SQLite (Execute SQL Tab)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. SELECT: Browse all available found items (Student/Public View)
-- ----------------------------------------------------------------------------
SELECT 
    found_item_id,
    item_name,
    description,
    found_location,
    found_date,
    status
FROM found_items
WHERE status = 'AVAILABLE'
ORDER BY found_item_id DESC;


-- ----------------------------------------------------------------------------
-- 2. INSERT: Report a new lost item (Student Action)
-- ----------------------------------------------------------------------------
INSERT INTO lost_items (
    user_id,
    item_name,
    category,
    description,
    lost_location,
    lost_date,
    status
) VALUES (
    1,
    'DBMS Book',
    'Books & Stationery',
    'Blue cover DBMS textbook with lecture notes',
    'Computer Lab 3',
    '25-08-2026',
    'SEARCHING'
);


-- ----------------------------------------------------------------------------
-- 3. DELETE: Remove a found item from inventory (Student/Public Action)
-- Demonstrates Parameterized SQL DELETE
-- ----------------------------------------------------------------------------
DELETE FROM found_items
WHERE found_item_id = 1;


-- ----------------------------------------------------------------------------
-- 4. SELECT: View lost reports for a specific student (Rahul, user_id=1)
-- ----------------------------------------------------------------------------
SELECT 
    lost_item_id,
    item_name,
    category,
    description,
    lost_location,
    lost_date,
    status,
    created_at
FROM lost_items
WHERE user_id = 1
ORDER BY lost_item_id DESC;


-- ----------------------------------------------------------------------------
-- 5. JOIN: Admin View &mdash; Relational JOIN between users and lost_items
-- Demonstrates Foreign Key relationship (lost_items.user_id = users.user_id)
-- ----------------------------------------------------------------------------
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


-- ----------------------------------------------------------------------------
-- 6. UPDATE: Mark a lost item as FOUND (Admin Action)
-- ----------------------------------------------------------------------------
UPDATE lost_items
SET status = 'FOUND'
WHERE lost_item_id = 1;


-- ----------------------------------------------------------------------------
-- 7. INSERT: Create automated student notification after status update
-- ----------------------------------------------------------------------------
INSERT INTO notifications (
    user_id,
    message,
    is_read
) VALUES (
    1,
    'Your HP Laptop Charger 65W has been found. Please visit the Lost & Found Department.',
    0
);


-- ----------------------------------------------------------------------------
-- 8. SELECT: Retrieve all notifications for a student
-- ----------------------------------------------------------------------------
SELECT 
    notification_id,
    message,
    is_read,
    created_at
FROM notifications
WHERE user_id = 1
ORDER BY notification_id DESC;
