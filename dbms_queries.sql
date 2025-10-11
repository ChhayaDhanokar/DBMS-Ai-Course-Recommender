image.png-- =====================================================
-- AI COURSE RECOMMENDATION SYSTEM - DBMS CONCEPTS DEMONSTRATION
-- =====================================================
-- DBMS Mini Project - Complete Query Examples
-- Author: Student
-- Date: October 2025
-- Description: Comprehensive demonstration of all DBMS concepts
-- Covers: DDL, DML, DQL, DCL, TCL with practical examples
-- =====================================================

-- =====================================================
-- 1. DDL (DATA DEFINITION LANGUAGE)
-- =====================================================

-- CREATE TABLE Example
-- Creating a temporary table to track course prerequisites
CREATE TABLE course_prerequisites (
    prerequisite_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    prerequisite_course_id INT NOT NULL,
    is_mandatory BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (prerequisite_course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_prerequisite (course_id, prerequisite_course_id)
);

-- ALTER TABLE Examples
-- Add a new column to track student's preferred learning mode
ALTER TABLE students 
ADD COLUMN preferred_learning_mode ENUM('Online', 'Offline', 'Hybrid') DEFAULT 'Online';

-- Modify existing column to increase phone number length
ALTER TABLE students 
MODIFY COLUMN phone VARCHAR(20);

-- Add a column to track course instructor
ALTER TABLE courses 
ADD COLUMN instructor_name VARCHAR(100) DEFAULT 'TBA';

-- Add a column to track course price
ALTER TABLE courses 
ADD COLUMN price DECIMAL(10,2) DEFAULT 0.00;

-- Drop a column example (removing the price column we just added)
ALTER TABLE courses 
DROP COLUMN price;

-- CREATE INDEX Examples
-- Index for faster course search by instructor
CREATE INDEX idx_courses_instructor ON courses(instructor_name);

-- Composite index for enrollment queries by date and status
CREATE INDEX idx_enrollments_date_status ON enrollments(enrollment_date, completion_status);

-- Index for faster feedback queries by rating
CREATE INDEX idx_feedback_rating_date ON feedback(rating, feedback_date);

-- DROP TABLE Example
-- Drop the temporary prerequisites table
DROP TABLE IF EXISTS course_prerequisites;

-- TRUNCATE TABLE Example
-- Create a temporary log table and then truncate it
CREATE TABLE temp_activity_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    activity VARCHAR(255),
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some test data
INSERT INTO temp_activity_log (activity) VALUES 
('User login'), ('Course enrollment'), ('Feedback submitted');

-- Show data before truncate
SELECT 'Data before TRUNCATE:' AS Info;
SELECT * FROM temp_activity_log;

-- Truncate the table (removes all data but keeps structure)
TRUNCATE TABLE temp_activity_log;

-- Show empty table after truncate
SELECT 'Data after TRUNCATE:' AS Info;
SELECT * FROM temp_activity_log;

-- Clean up
DROP TABLE temp_activity_log;

-- =====================================================
-- 2. DML (DATA MANIPULATION LANGUAGE)
-- =====================================================

-- INSERT Examples

-- Insert a new student
INSERT INTO students (name, email, password, phone, department, year, preferred_learning_mode) 
VALUES ('Rajesh Khanna', 'rajesh.khanna@college.edu', 'password123', '+91-9876543225', 'Computer Science', '2nd Year', 'Hybrid');

-- Insert a new course
INSERT INTO courses (course_name, description, category, duration_hours, difficulty_level, instructor_name) 
VALUES ('Blockchain Development', 'Learn blockchain technology, smart contracts, and cryptocurrency development using Solidity and Web3.', 'Blockchain', 75, 'Advanced', 'Dr. Blockchain Expert');

-- Insert a new skill
INSERT INTO skills (skill_name, category) 
VALUES ('Blockchain', 'Emerging Technology');

-- Insert multiple enrollments at once
INSERT INTO enrollments (student_id, course_id, completion_status) VALUES 
(16, 1, 'Enrolled'),  -- New student in MERN course
(1, 13, 'Enrolled');  -- Arjun in new Blockchain course

-- Insert student skill
INSERT INTO student_skills (student_id, skill_id, proficiency_level) 
VALUES (16, 1, 'Beginner');  -- New student has beginner Python

-- UPDATE Examples

-- Update course average rating after new feedback
UPDATE courses 
SET average_rating = 4.8, total_enrollments = total_enrollments + 1 
WHERE course_id = 5;

-- Update student information
UPDATE students 
SET phone = '+91-9876543226', preferred_learning_mode = 'Online' 
WHERE student_id = 1;

-- Update enrollment status to completed
UPDATE enrollments 
SET completion_status = 'Completed', completion_date = NOW() 
WHERE enrollment_id = 16;

-- Update multiple students' department (bulk update)
UPDATE students 
SET department = 'Computer Science and Engineering' 
WHERE department = 'Computer Science' AND year = '4th Year';

-- Update course instructor for multiple courses
UPDATE courses 
SET instructor_name = 'Prof. Web Development Expert' 
WHERE category = 'Web Development' AND instructor_name = 'TBA';

-- DELETE Examples

-- Delete old feedback (older than 1 year)
DELETE FROM feedback 
WHERE feedback_date < DATE_SUB(NOW(), INTERVAL 1 YEAR);

-- Delete inactive enrollments (enrolled but no progress for 6 months)
DELETE FROM enrollments 
WHERE completion_status = 'Enrolled' 
AND enrollment_date < DATE_SUB(NOW(), INTERVAL 6 MONTH);

-- Delete students who haven't enrolled in any course
DELETE FROM students 
WHERE student_id NOT IN (SELECT DISTINCT student_id FROM enrollments);

-- =====================================================
-- 3. DQL (DATA QUERY LANGUAGE)
-- =====================================================

-- Simple SELECT Queries

-- Get all students
SELECT 'All Students:' AS Info;
SELECT student_id, name, email, department, year FROM students;

-- Get all courses with basic info
SELECT 'All Courses:' AS Info;
SELECT course_id, course_name, category, difficulty_level, average_rating FROM courses;

-- Get all available skills
SELECT 'All Skills:' AS Info;
SELECT skill_id, skill_name, category FROM skills;

-- Get all completed enrollments
SELECT 'Completed Enrollments:' AS Info;
SELECT enrollment_id, student_id, course_id, completion_date FROM enrollments WHERE completion_status = 'Completed';

-- Get all high-rated feedback
SELECT 'High-Rated Feedback:' AS Info;
SELECT feedback_id, student_id, course_id, rating, LEFT(review_text, 50) AS review_preview FROM feedback WHERE rating >= 4;

-- WHERE Clause Examples

-- Students from Computer Science department
SELECT 'CS Students:' AS Info;
SELECT name, email, year FROM students WHERE department = 'Computer Science';

-- Intermediate level courses
SELECT 'Intermediate Courses:' AS Info;
SELECT course_name, category, duration_hours FROM courses WHERE difficulty_level = 'Intermediate';

-- Students with advanced proficiency in any skill
SELECT 'Advanced Skill Students:' AS Info;
SELECT DISTINCT s.name, s.department FROM students s 
JOIN student_skills ss ON s.student_id = ss.student_id 
WHERE ss.proficiency_level = 'Advanced';

-- Courses with high ratings and many enrollments
SELECT 'Popular High-Rated Courses:' AS Info;
SELECT course_name, average_rating, total_enrollments FROM courses 
WHERE average_rating >= 4.5 AND total_enrollments >= 15;

-- Recent enrollments (last 30 days)
SELECT 'Recent Enrollments:' AS Info;
SELECT s.name, c.course_name, e.enrollment_date FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id
WHERE e.enrollment_date >= DATE_SUB(NOW(), INTERVAL 30 DAY);

-- ORDER BY and LIMIT Examples

-- Top 5 highest rated courses
SELECT 'Top 5 Highest Rated Courses:' AS Info;
SELECT course_name, average_rating, total_enrollments FROM courses 
ORDER BY average_rating DESC, total_enrollments DESC LIMIT 5;

-- Latest 3 student registrations
SELECT 'Latest Student Registrations:' AS Info;
SELECT name, email, department, registration_date FROM students 
ORDER BY registration_date DESC LIMIT 3;

-- Courses sorted by duration (shortest first)
SELECT 'Courses by Duration:' AS Info;
SELECT course_name, duration_hours, difficulty_level FROM courses 
ORDER BY duration_hours ASC, course_name ASC;

-- INNER JOIN Examples

-- Students with their enrolled courses
SELECT 'Students and Their Courses:' AS Info;
SELECT s.name AS student_name, c.course_name, e.completion_status, e.enrollment_date
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id
ORDER BY s.name, e.enrollment_date;

-- Courses with their required skills
SELECT 'Courses and Required Skills:' AS Info;
SELECT c.course_name, sk.skill_name, c.difficulty_level
FROM courses c
INNER JOIN course_skills cs ON c.course_id = cs.course_id
INNER JOIN skills sk ON cs.skill_id = sk.skill_id
ORDER BY c.course_name, sk.skill_name;

-- Students with their skills and proficiency
SELECT 'Students and Their Skills:' AS Info;
SELECT s.name AS student_name, sk.skill_name, ss.proficiency_level, s.department
FROM students s
INNER JOIN student_skills ss ON s.student_id = ss.student_id
INNER JOIN skills sk ON ss.skill_id = sk.skill_id
ORDER BY s.name, sk.skill_name;

-- LEFT JOIN Examples

-- All students with their enrollment count (including students with no enrollments)
SELECT 'All Students with Enrollment Count:' AS Info;
SELECT s.name, s.department, s.year, COUNT(e.enrollment_id) AS total_enrollments
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.name, s.department, s.year
ORDER BY total_enrollments DESC;

-- All courses with their feedback count (including courses with no feedback)
SELECT 'All Courses with Feedback Count:' AS Info;
SELECT c.course_name, c.category, COUNT(f.feedback_id) AS feedback_count, c.average_rating
FROM courses c
LEFT JOIN feedback f ON c.course_id = f.course_id
GROUP BY c.course_id, c.course_name, c.category, c.average_rating
ORDER BY feedback_count DESC;

-- RIGHT JOIN Example

-- All skills with students who have them (including skills no student has)
SELECT 'All Skills with Student Count:' AS Info;
SELECT sk.skill_name, sk.category, COUNT(ss.student_id) AS student_count
FROM student_skills ss
RIGHT JOIN skills sk ON ss.skill_id = sk.skill_id
GROUP BY sk.skill_id, sk.skill_name, sk.category
ORDER BY student_count DESC;

-- Subquery Examples

-- Students who have enrolled in more than 2 courses
SELECT 'Students with >2 Enrollments:' AS Info;
SELECT s.name, s.department, 
       (SELECT COUNT(*) FROM enrollments e WHERE e.student_id = s.student_id) AS enrollment_count
FROM students s
WHERE (SELECT COUNT(*) FROM enrollments e WHERE e.student_id = s.student_id) > 2;

-- Courses with above average rating
SELECT 'Above Average Rated Courses:' AS Info;
SELECT course_name, average_rating, category
FROM courses
WHERE average_rating > (SELECT AVG(average_rating) FROM courses);

-- Students who have completed at least one course
SELECT 'Students with Completed Courses:' AS Info;
SELECT name, department FROM students
WHERE student_id IN (
    SELECT DISTINCT student_id FROM enrollments 
    WHERE completion_status = 'Completed'
);

-- Courses that have no enrollments
SELECT 'Courses with No Enrollments:' AS Info;
SELECT course_name, category, difficulty_level
FROM courses
WHERE course_id NOT IN (SELECT DISTINCT course_id FROM enrollments WHERE course_id IS NOT NULL);

-- Students with the most advanced skills
SELECT 'Students with Most Advanced Skills:' AS Info;
SELECT s.name, s.department,
       (SELECT COUNT(*) FROM student_skills ss WHERE ss.student_id = s.student_id AND ss.proficiency_level = 'Advanced') AS advanced_skills_count
FROM students s
WHERE (SELECT COUNT(*) FROM student_skills ss WHERE ss.student_id = s.student_id AND ss.proficiency_level = 'Advanced') > 0
ORDER BY advanced_skills_count DESC;

-- Aggregate Functions Examples

-- Count total students per department
SELECT 'Students per Department:' AS Info;
SELECT department, COUNT(*) AS student_count
FROM students
GROUP BY department;

-- Average rating per course category
SELECT 'Average Rating per Category:' AS Info;
SELECT category, AVG(average_rating) AS avg_category_rating, COUNT(*) AS course_count
FROM courses
GROUP BY category;

-- Maximum and minimum course duration
SELECT 'Course Duration Stats:' AS Info;
SELECT 
    MAX(duration_hours) AS longest_course,
    MIN(duration_hours) AS shortest_course,
    AVG(duration_hours) AS average_duration
FROM courses;

-- Total enrollments across all courses
SELECT 'Total Enrollment Stats:' AS Info;
SELECT 
    SUM(total_enrollments) AS total_all_enrollments,
    AVG(total_enrollments) AS avg_enrollments_per_course
FROM courses;

-- Count feedback by rating
SELECT 'Feedback Distribution:' AS Info;
SELECT rating, COUNT(*) AS feedback_count
FROM feedback
GROUP BY rating
ORDER BY rating DESC;

-- GROUP BY Examples

-- Courses per category with average rating
SELECT 'Courses per Category:' AS Info;
SELECT category, COUNT(*) AS course_count, AVG(average_rating) AS avg_rating
FROM courses
GROUP BY category
ORDER BY course_count DESC;

-- Students per year and department
SELECT 'Students by Year and Department:' AS Info;
SELECT department, year, COUNT(*) AS student_count
FROM students
GROUP BY department, year
ORDER BY department, year;

-- Enrollment status distribution
SELECT 'Enrollment Status Distribution:' AS Info;
SELECT completion_status, COUNT(*) AS count
FROM enrollments
GROUP BY completion_status;

-- Skills by category with proficiency breakdown
SELECT 'Skills by Category and Proficiency:' AS Info;
SELECT sk.category, ss.proficiency_level, COUNT(*) AS count
FROM skills sk
JOIN student_skills ss ON sk.skill_id = ss.skill_id
GROUP BY sk.category, ss.proficiency_level
ORDER BY sk.category, ss.proficiency_level;

-- HAVING Clause Examples

-- Categories with more than 2 courses
SELECT 'Categories with >2 Courses:' AS Info;
SELECT category, COUNT(*) AS course_count, AVG(average_rating) AS avg_rating
FROM courses
GROUP BY category
HAVING COUNT(*) > 2;

-- Departments with average student year > 2.5
SELECT 'Departments with Senior Students:' AS Info;
SELECT department, COUNT(*) AS student_count,
       AVG(CASE 
           WHEN year = '1st Year' THEN 1
           WHEN year = '2nd Year' THEN 2
           WHEN year = '3rd Year' THEN 3
           WHEN year = '4th Year' THEN 4
           WHEN year = 'Graduate' THEN 5
       END) AS avg_year_numeric
FROM students
GROUP BY department
HAVING AVG(CASE 
           WHEN year = '1st Year' THEN 1
           WHEN year = '2nd Year' THEN 2
           WHEN year = '3rd Year' THEN 3
           WHEN year = '4th Year' THEN 4
           WHEN year = 'Graduate' THEN 5
       END) > 2.5;

-- Complex Queries

-- Top 3 students by total completed courses with their details
SELECT 'Top Students by Completed Courses:' AS Info;
SELECT s.name, s.department, s.year, 
       COUNT(e.enrollment_id) AS completed_courses,
       AVG(f.rating) AS avg_feedback_given
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
LEFT JOIN feedback f ON s.student_id = f.student_id
WHERE e.completion_status = 'Completed'
GROUP BY s.student_id, s.name, s.department, s.year
ORDER BY completed_courses DESC, avg_feedback_given DESC
LIMIT 3;

-- Courses with no current enrollments but have historical data
SELECT 'Courses with No Active Enrollments:' AS Info;
SELECT c.course_name, c.category, c.total_enrollments AS historical_enrollments,
       COUNT(e.enrollment_id) AS current_active_enrollments
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id AND e.completion_status IN ('Enrolled', 'In Progress')
GROUP BY c.course_id, c.course_name, c.category, c.total_enrollments
HAVING COUNT(e.enrollment_id) = 0 AND c.total_enrollments > 0;

-- Comprehensive student dashboard query
SELECT 'Student Dashboard Data:' AS Info;
SELECT s.name, s.department, s.year,
       COUNT(DISTINCT e.course_id) AS total_enrollments,
       COUNT(DISTINCT CASE WHEN e.completion_status = 'Completed' THEN e.course_id END) AS completed_courses,
       COUNT(DISTINCT ss.skill_id) AS total_skills,
       COUNT(DISTINCT CASE WHEN ss.proficiency_level = 'Advanced' THEN ss.skill_id END) AS advanced_skills,
       AVG(f.rating) AS avg_rating_given
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
LEFT JOIN student_skills ss ON s.student_id = ss.student_id
LEFT JOIN feedback f ON s.student_id = f.student_id
WHERE s.student_id = 1  -- Example for student ID 1
GROUP BY s.student_id, s.name, s.department, s.year;

-- LIKE Operator Examples

-- Find courses with 'Development' in the name
SELECT 'Courses with Development:' AS Info;
SELECT course_name, category, difficulty_level
FROM courses
WHERE course_name LIKE '%Development%';

-- Find students with email containing 'college'
SELECT 'College Email Students:' AS Info;
SELECT name, email, department
FROM students
WHERE email LIKE '%college%';

-- BETWEEN Operator Example

-- Courses with duration between 40 and 70 hours
SELECT 'Medium Duration Courses:' AS Info;
SELECT course_name, duration_hours, category, difficulty_level
FROM courses
WHERE duration_hours BETWEEN 40 AND 70
ORDER BY duration_hours;

-- IN Operator Example

-- Students from specific departments
SELECT 'CS and IT Students:' AS Info;
SELECT name, department, year, email
FROM students
WHERE department IN ('Computer Science', 'Information Technology')
ORDER BY department, name;

-- CASE Statement Example

-- Categorize students by their skill level
SELECT 'Student Skill Level Categories:' AS Info;
SELECT s.name, s.department,
       COUNT(ss.skill_id) AS total_skills,
       CASE 
           WHEN COUNT(ss.skill_id) = 0 THEN 'No Skills'
           WHEN COUNT(ss.skill_id) BETWEEN 1 AND 2 THEN 'Beginner Level'
           WHEN COUNT(ss.skill_id) BETWEEN 3 AND 4 THEN 'Intermediate Level'
           WHEN COUNT(ss.skill_id) >= 5 THEN 'Advanced Level'
       END AS skill_category
FROM students s
LEFT JOIN student_skills ss ON s.student_id = ss.student_id
GROUP BY s.student_id, s.name, s.department
ORDER BY total_skills DESC;

-- =====================================================
-- 4. DCL (DATA CONTROL LANGUAGE)
-- =====================================================

-- Create Users
CREATE USER 'student_user'@'localhost' IDENTIFIED BY 'student123';
CREATE USER 'admin_user'@'localhost' IDENTIFIED BY 'admin123';

-- Grant Permissions

-- Student user gets read access to most tables and limited write access
GRANT SELECT ON course_recommendation_db.students TO 'student_user'@'localhost';
GRANT SELECT ON course_recommendation_db.courses TO 'student_user'@'localhost';
GRANT SELECT ON course_recommendation_db.skills TO 'student_user'@'localhost';
GRANT SELECT ON course_recommendation_db.course_skills TO 'student_user'@'localhost';
GRANT SELECT, INSERT, UPDATE ON course_recommendation_db.enrollments TO 'student_user'@'localhost';
GRANT SELECT, INSERT, UPDATE ON course_recommendation_db.student_skills TO 'student_user'@'localhost';
GRANT SELECT, INSERT ON course_recommendation_db.feedback TO 'student_user'@'localhost';

-- Admin user gets full access to all tables
GRANT ALL PRIVILEGES ON course_recommendation_db.* TO 'admin_user'@'localhost';

-- Grant specific permissions
GRANT CREATE, DROP ON course_recommendation_db.* TO 'admin_user'@'localhost';

-- Show Grants
SHOW GRANTS FOR 'student_user'@'localhost';
SHOW GRANTS FOR 'admin_user'@'localhost';

-- Revoke Permissions
-- Revoke UPDATE permission from student_user on enrollments
REVOKE UPDATE ON course_recommendation_db.enrollments FROM 'student_user'@'localhost';

-- Revoke INSERT permission from student_user on feedback
REVOKE INSERT ON course_recommendation_db.feedback FROM 'student_user'@'localhost';

-- Show grants after revoke
SHOW GRANTS FOR 'student_user'@'localhost';

-- =====================================================
-- 5. TCL (TRANSACTION CONTROL LANGUAGE)
-- =====================================================

-- Transaction Example with COMMIT
-- Scenario: Student enrolling in a course (must update both enrollments and course count)

START TRANSACTION;

-- Insert enrollment record
INSERT INTO enrollments (student_id, course_id, completion_status) 
VALUES (3, 4, 'Enrolled');

-- Update course enrollment count
UPDATE courses 
SET total_enrollments = total_enrollments + 1 
WHERE course_id = 4;

-- Check if everything looks good
SELECT 'Transaction Preview:' AS Info;
SELECT * FROM enrollments WHERE student_id = 3 AND course_id = 4;
SELECT course_name, total_enrollments FROM courses WHERE course_id = 4;

-- Commit the transaction
COMMIT;

SELECT 'Transaction Committed Successfully!' AS Status;

-- Transaction Example with ROLLBACK
-- Scenario: Attempting to enroll student in a course they're already enrolled in

START TRANSACTION;

-- Try to insert duplicate enrollment (this should be prevented by unique constraint)
-- But let's simulate a scenario where we want to rollback

INSERT INTO enrollments (student_id, course_id, completion_status) 
VALUES (1, 1, 'Enrolled');

-- Simulate checking some condition that fails
SELECT 'Checking enrollment validity...' AS Info;

-- Decide to rollback due to business logic failure
ROLLBACK;

SELECT 'Transaction Rolled Back!' AS Status;

-- Transaction with SAVEPOINT
-- Scenario: Complex operation with multiple steps and partial rollback

START TRANSACTION;

-- Step 1: Add a new skill
INSERT INTO skills (skill_name, category) 
VALUES ('Kubernetes', 'DevOps');

-- Create a savepoint after adding skill
SAVEPOINT after_skill_insert;

-- Step 2: Add this skill to a student
INSERT INTO student_skills (student_id, skill_id, proficiency_level) 
VALUES (1, (SELECT skill_id FROM skills WHERE skill_name = 'Kubernetes'), 'Beginner');

-- Create another savepoint
SAVEPOINT after_student_skill;

-- Step 3: Try to add the skill to a course (let's say this fails due to business logic)
INSERT INTO course_skills (course_id, skill_id) 
VALUES (8, (SELECT skill_id FROM skills WHERE skill_name = 'Kubernetes'));

-- Simulate a failure - rollback to the savepoint (keeping skill and student_skill)
ROLLBACK TO SAVEPOINT after_student_skill;

-- Check what we have after partial rollback
SELECT 'After Partial Rollback:' AS Info;
SELECT * FROM skills WHERE skill_name = 'Kubernetes';
SELECT * FROM student_skills WHERE skill_id = (SELECT skill_id FROM skills WHERE skill_name = 'Kubernetes');
SELECT * FROM course_skills WHERE skill_id = (SELECT skill_id FROM skills WHERE skill_name = 'Kubernetes');

-- Commit the remaining changes
COMMIT;

SELECT 'Transaction with Savepoint Completed!' AS Status;

-- =====================================================
-- CLEANUP SECTION
-- =====================================================

-- Remove the test users (optional - comment out if you want to keep them)
-- DROP USER 'student_user'@'localhost';
-- DROP USER 'admin_user'@'localhost';

-- Remove test columns added during DDL examples
ALTER TABLE students DROP COLUMN IF EXISTS preferred_learning_mode;
ALTER TABLE courses DROP COLUMN IF EXISTS instructor_name;

-- Remove test indexes
DROP INDEX IF EXISTS idx_courses_instructor ON courses;
DROP INDEX IF EXISTS idx_enrollments_date_status ON enrollments;
DROP INDEX IF EXISTS idx_feedback_rating_date ON feedback;

-- =====================================================
-- SUMMARY REPORT
-- =====================================================

SELECT '=== DBMS CONCEPTS DEMONSTRATION COMPLETE ===' AS Summary;

SELECT 'DDL Operations:' AS Category, 'CREATE, ALTER, DROP, TRUNCATE, INDEX' AS Operations_Covered
UNION ALL
SELECT 'DML Operations:', 'INSERT, UPDATE, DELETE with various conditions'
UNION ALL
SELECT 'DQL Operations:', 'SELECT, JOIN, Subqueries, Aggregates, GROUP BY, HAVING'
UNION ALL
SELECT 'DCL Operations:', 'CREATE USER, GRANT, REVOKE, SHOW GRANTS'
UNION ALL
SELECT 'TCL Operations:', 'START TRANSACTION, COMMIT, ROLLBACK, SAVEPOINT';

SELECT 'Total Query Examples:' AS Metric, '50+' AS Count
UNION ALL
SELECT 'Tables Used:', '8 Main Tables + Temporary Tables'
UNION ALL
SELECT 'Join Types:', 'INNER, LEFT, RIGHT'
UNION ALL
SELECT 'Advanced Features:', 'Subqueries, Aggregates, Complex Conditions';

-- =====================================================
-- END OF DBMS CONCEPTS DEMONSTRATION
-- =====================================================





