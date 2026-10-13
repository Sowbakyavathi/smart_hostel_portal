-- ============================================
-- CREATE DATABASE
-- ============================================
CREATE DATABASE IF NOT EXISTS smart_hostel_db;
USE smart_hostel_db;

-- ============================================
-- TABLES
-- ============================================

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    hostel_name VARCHAR(50),
    room_number VARCHAR(10),
    branch VARCHAR(100),
    phone VARCHAR(15),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE complaints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50) DEFAULT 'other',
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE notices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE leave_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    from_date DATE,
    to_date DATE,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE visitor_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    visitor_name VARCHAR(100) NOT NULL,
    purpose VARCHAR(200),
    check_in TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE mess_feedback (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    meal_type VARCHAR(20),
    rating INT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE rooms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    room_number VARCHAR(10) UNIQUE NOT NULL,
    hostel_name VARCHAR(50),
    floor INT,
    capacity INT,
    status VARCHAR(20) DEFAULT 'available'
);

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Rooms
INSERT INTO rooms (room_number, hostel_name, floor, capacity, status) VALUES
('101', 'Boys Hostel A', 1, 2, 'occupied'),
('102', 'Boys Hostel A', 1, 2, 'available'),
('201', 'Boys Hostel A', 2, 2, 'available'),
('301', 'Girls Hostel A', 1, 2, 'available');

-- Notices
INSERT INTO notices (title, content) VALUES
('Welcome to Smart Hostel', 'This is your hostel management portal. All notices will appear here.');
