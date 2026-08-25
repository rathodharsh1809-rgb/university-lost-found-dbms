-- ============================================================================
-- UNIVERSITY LOST & FOUND DEPARTMENT - DEMO SEED DATA
-- Seed dataset for Live Demo and DB Browser for SQLite inspection
-- ============================================================================

-- 1. Demo Users (Student and Admin)
INSERT INTO users (user_id, name, email, role) VALUES
(1, 'Rahul', 'rahul@university.edu', 'student'),
(2, 'Lost & Found Department', 'admin@university.edu', 'admin');

-- 2. Demo Found Items (Available on campus)
INSERT INTO found_items (found_item_id, item_name, description, found_location, found_date, status) VALUES
(1, 'Scientific Calculator TI-84', 'Blue casing with name sticker on back', 'Math Block Hall 2', '24-08-2026', 'AVAILABLE'),
(2, 'Water Bottle Hydro Flask', 'Matte black 32oz insulated bottle', 'Sports Gymnasium', '23-08-2026', 'AVAILABLE'),
(3, 'Silver Wrist Watch', 'Metal strap analog watch found near cafeteria', 'Student Center', '22-08-2026', 'AVAILABLE');

-- 3. Demo Initial Lost Item
INSERT INTO lost_items (lost_item_id, user_id, item_name, category, description, lost_location, lost_date, status) VALUES
(1, 1, 'HP Laptop Charger 65W', 'Electronics', 'Black USB-C fast charger forgotten on bench', 'Library 1st Floor', '24-08-2026', 'SEARCHING');

-- 4. Demo Notifications for Student (Rahul)
INSERT INTO notifications (notification_id, user_id, message, is_read) VALUES
(1, 1, 'Welcome to the University Lost & Found portal. You can track all your reports here.', 0);
