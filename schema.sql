-- =====================================================
-- AI COURSE RECOMMENDATION SYSTEM - DATABASE SCHEMA
-- =====================================================
-- DBMS Mini Project
-- Author: Student
-- Date: October 2025
-- Description: Complete database schema for course recommendation system
-- Tables: 8 tables in 3NF with proper constraints and relationships
-- =====================================================

-- Drop existing tables if they exist (for clean re-runs)
-- Order matters due to foreign key constraints
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS course_skills;
DROP TABLE IF EXISTS student_skills;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

-- =====================================================
-- TABLE 1: STUDENTS
-- =====================================================
-- Stores student information and credentials
-- Primary entity for the system users
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- Hashed password storage
    phone VARCHAR(15),
    department VARCHAR(100) NOT NULL,
    year ENUM('1st Year', '2nd Year', '3rd Year', '4th Year', 'Graduate') NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_email_format CHECK (email LIKE '%@%.%'),
    CONSTRAINT chk_phone_format CHECK (phone REGEXP '^[0-9+()-]{10,15}$')
);

-- =====================================================
-- TABLE 2: COURSES
-- =====================================================
-- Stores course information and metadata
-- Central entity for course catalog
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    duration_hours INT NOT NULL,
    difficulty_level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL,
    average_rating DECIMAL(3,2) DEFAULT 0.00,
    total_enrollments INT DEFAULT 0,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_duration_positive CHECK (duration_hours > 0),
    CONSTRAINT chk_rating_range CHECK (average_rating >= 0.00 AND average_rating <= 5.00),
    CONSTRAINT chk_enrollments_positive CHECK (total_enrollments >= 0)
);

-- =====================================================
-- TABLE 3: SKILLS
-- =====================================================
-- Master table for all available skills
-- Normalized to avoid skill name duplication
CREATE TABLE skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    
    -- Ensure skill names are not empty
    CONSTRAINT chk_skill_name_not_empty CHECK (TRIM(skill_name) != '')
);

-- =====================================================
-- TABLE 4: STUDENT_SKILLS (Junction Table)
-- =====================================================
-- Many-to-Many relationship between Students and Skills
-- Stores student's skill proficiency levels
CREATE TABLE student_skills (
    student_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite Primary Key
    PRIMARY KEY (student_id, skill_id),
    
    -- Foreign Key Constraints
    FOREIGN KEY (student_id) REFERENCES students(student_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =====================================================
-- TABLE 5: COURSE_SKILLS (Junction Table)
-- =====================================================
-- Many-to-Many relationship between Courses and Skills
-- Defines which skills are required for each course
CREATE TABLE course_skills (
    course_id INT NOT NULL,
    skill_id INT NOT NULL,
    
    -- Composite Primary Key
    PRIMARY KEY (course_id, skill_id),
    
    -- Foreign Key Constraints
    FOREIGN KEY (course_id) REFERENCES courses(course_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =====================================================
-- TABLE 6: ENROLLMENTS
-- =====================================================
-- Tracks student enrollments in courses
-- Handles enrollment lifecycle and completion tracking
CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_status ENUM('Enrolled', 'In Progress', 'Completed', 'Dropped') DEFAULT 'Enrolled',
    completion_date TIMESTAMP NULL,
    
    -- Unique constraint to prevent duplicate enrollments
    UNIQUE KEY unique_enrollment (student_id, course_id),
    
    -- Foreign Key Constraints
    FOREIGN KEY (student_id) REFERENCES students(student_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    
    -- Business Logic Constraints
    CONSTRAINT chk_completion_date CHECK (
        (completion_status = 'Completed' AND completion_date IS NOT NULL) OR 
        (completion_status != 'Completed' AND completion_date IS NULL)
    )
);

-- =====================================================
-- TABLE 7: FEEDBACK
-- =====================================================
-- Stores student reviews and ratings for courses
-- Used for calculating course average ratings
CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    rating INT NOT NULL,
    review_text TEXT,
    feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (student_id) REFERENCES students(student_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    
    -- Business Logic Constraints
    CONSTRAINT chk_rating_range_feedback CHECK (rating >= 1 AND rating <= 5),
    
    -- Unique constraint: One feedback per student per course
    UNIQUE KEY unique_feedback (student_id, course_id)
);

-- =====================================================
-- TABLE 8: ADMIN
-- =====================================================
-- Stores admin credentials for system management
-- Separate from students for security and role management
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- Hashed password storage
    role ENUM('Super Admin', 'Course Manager', 'Content Moderator') DEFAULT 'Course Manager',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    
    -- Constraints
    CONSTRAINT chk_username_length CHECK (CHAR_LENGTH(username) >= 3)
);

-- =====================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- =====================================================
-- These indexes will speed up frequently used queries

-- Index on student email for login queries
CREATE INDEX idx_students_email ON students(email);

-- Index on course category for filtering
CREATE INDEX idx_courses_category ON courses(category);

-- Index on course difficulty for filtering
CREATE INDEX idx_courses_difficulty ON courses(difficulty_level);

-- Index on course rating for sorting top courses
CREATE INDEX idx_courses_rating ON courses(average_rating DESC);

-- Composite index for student skills lookup
CREATE INDEX idx_student_skills_lookup ON student_skills(student_id, skill_id);

-- Composite index for course skills lookup
CREATE INDEX idx_course_skills_lookup ON course_skills(course_id, skill_id);

-- Index on enrollment status for filtering active enrollments
CREATE INDEX idx_enrollments_status ON enrollments(completion_status);

-- Index on enrollment date for chronological queries
CREATE INDEX idx_enrollments_date ON enrollments(enrollment_date);

-- Index on feedback rating for analytics
CREATE INDEX idx_feedback_rating ON feedback(rating);

-- Index on feedback date for recent reviews
CREATE INDEX idx_feedback_date ON feedback(feedback_date);

-- Index on skill category for grouping
CREATE INDEX idx_skills_category ON skills(category);

-- =====================================================
-- NORMALIZATION VERIFICATION
-- =====================================================
-- All tables are in Third Normal Form (3NF):
--
-- 1NF: All tables have atomic values, no repeating groups
-- 2NF: All non-key attributes fully depend on primary key
-- 3NF: No transitive dependencies (non-key attributes don't depend on other non-key attributes)
--
-- Examples:
-- - student_skills: Composite PK (student_id, skill_id), proficiency depends on both
-- - courses: average_rating could be calculated but stored for performance
-- - feedback: Separate table instead of storing in enrollments (different lifecycle)

-- =====================================================
-- FOREIGN KEY RELATIONSHIPS SUMMARY
-- =====================================================
-- students (1) ←→ (M) student_skills (M) ←→ (1) skills
-- courses (1) ←→ (M) course_skills (M) ←→ (1) skills  
-- students (1) ←→ (M) enrollments (M) ←→ (1) courses
-- students (1) ←→ (M) feedback (M) ←→ (1) courses
--
-- All relationships use CASCADE for referential integrity

-- =====================================================
-- END OF SCHEMA
-- =====================================================

-- Display success message
SELECT 'AI Course Recommendation System Database Schema Created Successfully!' AS Status;

-- Show all created tables
SHOW TABLES;
