-- ============================================================================
-- UNIVERSITY LOST & FOUND DEPARTMENT - DBMS SCHEMA
-- SQLite Database Schema for Academic Project
-- Compatible with DB Browser for SQLite
-- ============================================================================

PRAGMA foreign_keys = OFF;

-- Drop existing tables in reverse dependency order
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS found_items;
DROP TABLE IF EXISTS lost_items;
DROP TABLE IF EXISTS users;

PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'faculty', 'admin'))
);

-- 2. Lost Items Table
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

-- 3. Found Items Table
CREATE TABLE found_items (
    found_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    description TEXT,
    found_location TEXT,
    found_date TEXT,
    status TEXT DEFAULT 'AVAILABLE' CHECK(status IN ('AVAILABLE', 'CLAIMED', 'DISPOSED')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 4. Notifications Table
CREATE TABLE notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    is_read INTEGER DEFAULT 0 CHECK(is_read IN (0, 1)),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Physical Indexes (Internal Level performance tuning)
CREATE INDEX IF NOT EXISTS idx_lost_items_user ON lost_items(user_id);
CREATE INDEX IF NOT EXISTS idx_lost_items_status ON lost_items(status);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
