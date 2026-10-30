-- ============================================================================
-- UNIVERSITY LOST & FOUND DEPARTMENT - DEMO SEED DATA
-- Seed dataset for Live Demo and DB Browser for SQLite inspection
-- ============================================================================

-- 1. Demo Users (Students, Faculty, and Admin)
INSERT INTO users (user_id, name, email, role) VALUES
(1, 'Rahul Verma', 'rahul@university.edu', 'student'),
(2, 'Lost & Found Department', 'admin@university.edu', 'admin'),
(3, 'Prof. Robert Jenkins', 'rjenkins@university.edu', 'faculty'),
(4, 'Sarah Chen', 'schen@university.edu', 'student'),
(5, 'Marcus Taylor', 'mtaylor@university.edu', 'student');

-- 2. Demo Found Items (Turned in to department)
INSERT INTO found_items (found_item_id, item_name, description, found_location, found_date, status) VALUES
(1, 'Scientific Calculator TI-84 Plus', 'Blue casing with student name sticker on reverse', 'Math Block Hall 2', '24-08-2026', 'AVAILABLE'),
(2, 'Water Bottle Hydro Flask', 'Matte black 32oz insulated stainless bottle', 'Sports Gymnasium', '23-08-2026', 'AVAILABLE'),
(3, 'Silver Wrist Watch Seiko', 'Metal link strap analog watch found near cafeteria counter', 'Student Center', '22-08-2026', 'AVAILABLE'),
(4, 'Black Leather Wallet', 'Contains campus transit card and student discount pass', 'Student Dining Hall', '23-08-2026', 'AVAILABLE'),
(5, 'Sony Wireless Headphones WH-1000XM4', 'Silver noise-cancelling headphones in zip case', 'Central Library Room 302', '24-08-2026', 'AVAILABLE'),
(6, 'Blue Spiral Notebook', 'Data Structures & Algorithms lecture notes and sketches', 'Computer Science Lab 4', '25-08-2026', 'CLAIMED'),
(7, 'Hydro Flask Travel Mug 16oz', 'Olive green commuter mug with sip lid', 'Auditorium North Wing', '21-08-2026', 'AVAILABLE');

-- 3. Demo Lost Items (Reported by students & faculty)
INSERT INTO lost_items (lost_item_id, user_id, item_name, category, description, lost_location, lost_date, status) VALUES
(1, 1, 'HP Laptop Charger 65W USB-C', 'Electronics', 'Black fast charger forgotten on study carrel desk', 'Library 1st Floor', '24-08-2026', 'SEARCHING'),
(2, 4, 'MacBook Air M2 13-inch', 'Electronics', 'Space Gray with computer science club stickers on lid', 'Central Library 3rd Floor', '24-08-2026', 'FOUND'),
(3, 3, 'Wireless Presentation Clicker', 'Electronics', 'Logitech red laser presenter used in lecture hall', 'Physics Lecture Hall 101', '22-08-2026', 'SEARCHING'),
(4, 5, 'Campus Smart ID Card & Lanyard', 'Identification & Cards', 'Student RFID badge inside blue university lanyard', 'Sports Gymnasium', '25-08-2026', 'COLLECTED'),
(5, 1, 'Organic Chemistry Lab Binder', 'Books & Stationery', 'Green 3-ring binder containing reaction diagrams', 'Chemistry Block Lab 3', '23-08-2026', 'SEARCHING');

-- 4. Demo Notifications
INSERT INTO notifications (notification_id, user_id, message, is_read) VALUES
(1, 1, 'Welcome to the University Lost & Found portal. You can track all your reports here.', 1),
(2, 4, 'Good news! Your lost MacBook Air M2 has been found by campus staff. Please visit Admin desk.', 1),
(3, 5, 'Your Campus Smart ID Card & Lanyard has been marked as collected.', 1),
(4, 1, 'Reminder: Your reported HP Laptop Charger is actively being searched for.', 0);

