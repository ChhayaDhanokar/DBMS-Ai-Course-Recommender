-- =====================================================
-- AI COURSE RECOMMENDATION SYSTEM - SAMPLE DATA
-- =====================================================
-- DBMS Mini Project - Sample Data Insertion
-- Author: Student
-- Date: October 2025
-- Description: Realistic sample data for testing the course recommendation system
-- =====================================================

-- Clear existing data (if any) in correct order due to foreign key constraints
DELETE FROM feedback;
DELETE FROM enrollments;
DELETE FROM course_skills;
DELETE FROM student_skills;
DELETE FROM admin;
DELETE FROM skills;
DELETE FROM courses;
DELETE FROM students;

-- Reset AUTO_INCREMENT counters
ALTER TABLE students AUTO_INCREMENT = 1;
ALTER TABLE courses AUTO_INCREMENT = 1;
ALTER TABLE skills AUTO_INCREMENT = 1;
ALTER TABLE enrollments AUTO_INCREMENT = 1;
ALTER TABLE feedback AUTO_INCREMENT = 1;
ALTER TABLE admin AUTO_INCREMENT = 1;

-- =====================================================
-- STUDENTS DATA (15 Students)
-- =====================================================
-- Diverse students from different departments and years
INSERT INTO students (name, email, password, phone, department, year) VALUES
-- Computer Science Students
('Arjun Sharma', 'arjun.sharma@college.edu', 'password123', '+91-9876543210', 'Computer Science', '3rd Year'),
('Priya Patel', 'priya.patel@college.edu', 'password123', '+91-9876543211', 'Computer Science', '4th Year'),
('Rohit Kumar', 'rohit.kumar@college.edu', 'password123', '+91-9876543212', 'Computer Science', '2nd Year'),
('Sneha Gupta', 'sneha.gupta@college.edu', 'password123', '+91-9876543213', 'Computer Science', '3rd Year'),

-- Information Technology Students
('Vikram Singh', 'vikram.singh@college.edu', 'password123', '+91-9876543214', 'Information Technology', '4th Year'),
('Ananya Reddy', 'ananya.reddy@college.edu', 'password123', '+91-9876543215', 'Information Technology', '2nd Year'),
('Karthik Nair', 'karthik.nair@college.edu', 'password123', '+91-9876543216', 'Information Technology', '3rd Year'),
('Pooja Jain', 'pooja.jain@college.edu', 'password123', '+91-9876543217', 'Information Technology', '1st Year'),

-- Electronics Students
('Aditya Verma', 'aditya.verma@college.edu', 'password123', '+91-9876543218', 'Electronics', '3rd Year'),
('Kavya Iyer', 'kavya.iyer@college.edu', 'password123', '+91-9876543219', 'Electronics', '2nd Year'),
('Rahul Agarwal', 'rahul.agarwal@college.edu', 'password123', '+91-9876543220', 'Electronics', '4th Year'),

-- Graduate Students
('Deepika Mehta', 'deepika.mehta@college.edu', 'password123', '+91-9876543221', 'Computer Science', 'Graduate'),
('Sanjay Rao', 'sanjay.rao@college.edu', 'password123', '+91-9876543222', 'Information Technology', 'Graduate'),

-- Mixed Departments
('Neha Bansal', 'neha.bansal@college.edu', 'password123', '+91-9876543223', 'Electronics', '1st Year'),
('Amit Thakur', 'amit.thakur@college.edu', 'password123', '+91-9876543224', 'Computer Science', '1st Year');

-- =====================================================
-- SKILLS DATA (15 Skills)
-- =====================================================
-- Comprehensive skill set covering various technology domains
INSERT INTO skills (skill_name, category) VALUES
-- Programming Languages
('Python', 'Programming'),
('JavaScript', 'Programming'),
('Java', 'Programming'),
('C++', 'Programming'),

-- Web Development
('HTML/CSS', 'Web Development'),
('React', 'Web Development'),
('Node.js', 'Web Development'),
('Angular', 'Web Development'),

-- Data & AI
('SQL', 'Database'),
('Machine Learning', 'Artificial Intelligence'),
('Data Analysis', 'Data Science'),
('Deep Learning', 'Artificial Intelligence'),

-- DevOps & Tools
('Docker', 'DevOps'),
('Git/GitHub', 'Development Tools'),

-- Design
('UI/UX Design', 'Design');

-- =====================================================
-- COURSES DATA (12 Courses)
-- =====================================================
-- Realistic courses across different categories and difficulty levels
INSERT INTO courses (course_name, description, category, duration_hours, difficulty_level, average_rating, total_enrollments) VALUES

-- Web Development Courses
('Full Stack Web Development with MERN', 'Complete web development course covering MongoDB, Express.js, React, and Node.js. Build real-world applications from scratch.', 'Web Development', 80, 'Intermediate', 4.5, 25),
('Frontend Development with React', 'Master modern React development including hooks, context API, and state management. Build responsive user interfaces.', 'Web Development', 60, 'Beginner', 4.3, 30),
('Backend API Development with Node.js', 'Learn to build scalable REST APIs using Node.js, Express, and MongoDB. Includes authentication and deployment.', 'Web Development', 50, 'Intermediate', 4.4, 20),

-- AI/ML Courses
('Machine Learning Fundamentals', 'Introduction to machine learning algorithms, supervised and unsupervised learning, and practical implementation in Python.', 'AI/ML', 70, 'Intermediate', 4.6, 18),
('Deep Learning with TensorFlow', 'Advanced deep learning concepts including neural networks, CNNs, RNNs, and practical projects using TensorFlow.', 'AI/ML', 90, 'Advanced', 4.7, 12),

-- Data Science Courses
('Data Analysis with Python', 'Comprehensive data analysis using pandas, numpy, matplotlib, and seaborn. Work with real datasets and create visualizations.', 'Data Science', 55, 'Beginner', 4.2, 28),
('SQL for Data Science', 'Master SQL for data analysis including complex queries, joins, window functions, and database optimization techniques.', 'Database', 40, 'Beginner', 4.4, 35),

-- DevOps Courses
('Docker and Containerization', 'Learn containerization with Docker, Docker Compose, and container orchestration. Deploy applications efficiently.', 'DevOps', 35, 'Intermediate', 4.1, 15),
('Git Version Control Mastery', 'Complete Git workflow including branching, merging, rebasing, and collaborative development using GitHub.', 'DevOps', 25, 'Beginner', 4.0, 40),

-- Design Course
('UI/UX Design Principles', 'Learn user interface and user experience design principles, wireframing, prototyping, and design tools like Figma.', 'Design', 45, 'Beginner', 4.3, 22),

-- Security Course
('Web Application Security', 'Comprehensive web security covering OWASP top 10, authentication, authorization, and secure coding practices.', 'Security', 60, 'Advanced', 4.5, 10),

-- Database Course
('Advanced Database Design', 'Master database design principles, normalization, indexing, query optimization, and NoSQL databases.', 'Database', 65, 'Advanced', 4.6, 8);

-- =====================================================
-- STUDENT_SKILLS DATA
-- =====================================================
-- Link students with their skills (2-4 skills per student with varying proficiency)
INSERT INTO student_skills (student_id, skill_id, proficiency_level) VALUES
-- Arjun Sharma (CS 3rd Year) - Full Stack Developer
(1, 1, 'Advanced'),    -- Python
(1, 2, 'Intermediate'), -- JavaScript
(1, 6, 'Advanced'),    -- React
(1, 9, 'Intermediate'), -- SQL

-- Priya Patel (CS 4th Year) - AI/ML Enthusiast
(2, 1, 'Advanced'),    -- Python
(2, 10, 'Advanced'),   -- Machine Learning
(2, 11, 'Intermediate'), -- Data Analysis
(2, 12, 'Beginner'),   -- Deep Learning

-- Rohit Kumar (CS 2nd Year) - Beginner Programmer
(3, 3, 'Intermediate'), -- Java
(3, 4, 'Beginner'),    -- C++
(3, 14, 'Beginner'),   -- Git/GitHub

-- Sneha Gupta (CS 3rd Year) - Web Developer
(4, 2, 'Advanced'),    -- JavaScript
(4, 5, 'Advanced'),    -- HTML/CSS
(4, 6, 'Intermediate'), -- React
(4, 15, 'Intermediate'), -- UI/UX Design

-- Vikram Singh (IT 4th Year) - DevOps Engineer
(5, 1, 'Intermediate'), -- Python
(5, 13, 'Advanced'),   -- Docker
(5, 14, 'Advanced'),   -- Git/GitHub
(5, 7, 'Intermediate'), -- Node.js

-- Ananya Reddy (IT 2nd Year) - Data Enthusiast
(6, 1, 'Beginner'),    -- Python
(6, 9, 'Intermediate'), -- SQL
(6, 11, 'Beginner'),   -- Data Analysis

-- Karthik Nair (IT 3rd Year) - Full Stack Developer
(7, 2, 'Advanced'),    -- JavaScript
(7, 7, 'Advanced'),    -- Node.js
(7, 8, 'Intermediate'), -- Angular
(7, 9, 'Intermediate'), -- SQL

-- Pooja Jain (IT 1st Year) - Beginner
(8, 5, 'Beginner'),    -- HTML/CSS
(8, 2, 'Beginner'),    -- JavaScript
(8, 14, 'Beginner'),   -- Git/GitHub

-- Aditya Verma (Electronics 3rd Year) - Programming Basics
(9, 4, 'Intermediate'), -- C++
(9, 1, 'Beginner'),    -- Python
(9, 3, 'Beginner'),    -- Java

-- Kavya Iyer (Electronics 2nd Year) - Web Design
(10, 5, 'Intermediate'), -- HTML/CSS
(10, 15, 'Advanced'),   -- UI/UX Design
(10, 2, 'Beginner'),    -- JavaScript

-- Rahul Agarwal (Electronics 4th Year) - Data Analysis
(11, 1, 'Intermediate'), -- Python
(11, 11, 'Advanced'),   -- Data Analysis
(11, 9, 'Intermediate'), -- SQL

-- Deepika Mehta (CS Graduate) - AI Researcher
(12, 1, 'Advanced'),    -- Python
(12, 10, 'Advanced'),   -- Machine Learning
(12, 12, 'Advanced'),   -- Deep Learning
(12, 11, 'Advanced'),   -- Data Analysis

-- Sanjay Rao (IT Graduate) - Senior Developer
(13, 2, 'Advanced'),    -- JavaScript
(13, 6, 'Advanced'),    -- React
(13, 7, 'Advanced'),    -- Node.js
(13, 13, 'Intermediate'), -- Docker

-- Neha Bansal (Electronics 1st Year) - Beginner
(14, 5, 'Beginner'),    -- HTML/CSS
(14, 15, 'Beginner'),   -- UI/UX Design

-- Amit Thakur (CS 1st Year) - Programming Beginner
(15, 1, 'Beginner'),    -- Python
(15, 3, 'Beginner'),    -- Java
(15, 14, 'Beginner');   -- Git/GitHub

-- =====================================================
-- COURSE_SKILLS DATA
-- =====================================================
-- Link courses with required skills (2-3 skills per course)
INSERT INTO course_skills (course_id, skill_id) VALUES
-- Full Stack Web Development with MERN
(1, 2),  -- JavaScript
(1, 6),  -- React
(1, 7),  -- Node.js

-- Frontend Development with React
(2, 5),  -- HTML/CSS
(2, 2),  -- JavaScript
(2, 6),  -- React

-- Backend API Development with Node.js
(3, 2),  -- JavaScript
(3, 7),  -- Node.js
(3, 9),  -- SQL

-- Machine Learning Fundamentals
(4, 1),  -- Python
(4, 10), -- Machine Learning
(4, 11), -- Data Analysis

-- Deep Learning with TensorFlow
(5, 1),  -- Python
(5, 10), -- Machine Learning
(5, 12), -- Deep Learning

-- Data Analysis with Python
(6, 1),  -- Python
(6, 11), -- Data Analysis

-- SQL for Data Science
(7, 9),  -- SQL
(7, 11), -- Data Analysis

-- Docker and Containerization
(8, 13), -- Docker
(8, 14), -- Git/GitHub

-- Git Version Control Mastery
(9, 14), -- Git/GitHub

-- UI/UX Design Principles
(10, 15), -- UI/UX Design
(10, 5),  -- HTML/CSS

-- Web Application Security
(11, 2),  -- JavaScript
(11, 1),  -- Python
(11, 9),  -- SQL

-- Advanced Database Design
(12, 9),  -- SQL
(12, 1);  -- Python

-- =====================================================
-- ENROLLMENTS DATA (20 Enrollments)
-- =====================================================
-- Random enrollments with different completion statuses
INSERT INTO enrollments (student_id, course_id, completion_status, completion_date) VALUES
-- Completed Enrollments (for feedback)
(1, 2, 'Completed', '2024-09-15 10:30:00'),  -- Arjun -> React Course
(1, 3, 'Completed', '2024-08-20 14:45:00'),  -- Arjun -> Node.js Course
(2, 4, 'Completed', '2024-09-10 16:20:00'),  -- Priya -> ML Fundamentals
(2, 5, 'Completed', '2024-07-25 11:15:00'),  -- Priya -> Deep Learning
(4, 2, 'Completed', '2024-09-05 13:30:00'),  -- Sneha -> React Course
(5, 8, 'Completed', '2024-08-30 15:45:00'),  -- Vikram -> Docker Course
(6, 6, 'Completed', '2024-09-12 12:20:00'),  -- Ananya -> Data Analysis
(7, 1, 'Completed', '2024-08-15 17:30:00'),  -- Karthik -> MERN Stack
(11, 6, 'Completed', '2024-09-08 14:15:00'), -- Rahul -> Data Analysis
(12, 5, 'Completed', '2024-07-30 16:45:00'), -- Deepika -> Deep Learning
(13, 1, 'Completed', '2024-08-25 10:20:00'), -- Sanjay -> MERN Stack
(3, 9, 'Completed', '2024-09-18 11:30:00'),  -- Rohit -> Git Course
(10, 10, 'Completed', '2024-09-01 15:15:00'), -- Kavya -> UI/UX Design
(8, 9, 'Completed', '2024-09-20 13:45:00'),  -- Pooja -> Git Course
(15, 9, 'Completed', '2024-09-22 12:30:00'), -- Amit -> Git Course

-- In Progress Enrollments
(1, 4, 'In Progress', NULL),   -- Arjun -> ML Fundamentals
(3, 2, 'In Progress', NULL),   -- Rohit -> React Course
(4, 10, 'In Progress', NULL),  -- Sneha -> UI/UX Design
(6, 7, 'In Progress', NULL),   -- Ananya -> SQL Course

-- Recently Enrolled
(9, 6, 'Enrolled', NULL);      -- Aditya -> Data Analysis

-- =====================================================
-- FEEDBACK DATA (15 Feedback Entries)
-- =====================================================
-- Feedback only for completed courses with ratings 3-5
INSERT INTO feedback (student_id, course_id, rating, review_text) VALUES
(1, 2, 5, 'Excellent React course! The instructor explained concepts clearly and the projects were very practical. Highly recommended for anyone wanting to learn modern frontend development.'),
(1, 3, 4, 'Great Node.js course with good coverage of API development. Could use more advanced topics but overall very satisfied with the content and teaching quality.'),
(2, 4, 5, 'Outstanding machine learning course! Perfect balance of theory and practical implementation. The Python exercises really helped solidify the concepts.'),
(2, 5, 5, 'Amazing deep learning course! Very comprehensive coverage of neural networks and TensorFlow. Challenging but extremely rewarding. Best course I have taken!'),
(4, 2, 4, 'Good React course for beginners. The pace was perfect and the projects were engaging. Would like to see more advanced React patterns covered.'),
(5, 8, 4, 'Solid Docker course with practical examples. Learned a lot about containerization and deployment. The hands-on labs were particularly helpful.'),
(6, 6, 3, 'Decent data analysis course but could be more comprehensive. Good introduction to pandas and matplotlib but lacks advanced statistical analysis.'),
(7, 1, 5, 'Fantastic MERN stack course! Comprehensive coverage from frontend to backend. The final project was challenging and really brought everything together.'),
(11, 6, 4, 'Good Python data analysis course. Well-structured content and practical examples. The visualization section was particularly useful for my projects.'),
(12, 5, 5, 'Exceptional deep learning course! As a graduate student, I found the advanced concepts well-explained and the research paper discussions very valuable.'),
(13, 1, 4, 'Excellent full-stack course with real-world applications. Good coverage of modern development practices. Would recommend for experienced developers.'),
(3, 9, 4, 'Very helpful Git course for beginners. Clear explanations of version control concepts and practical exercises. Essential for any developer.'),
(10, 10, 5, 'Amazing UI/UX design course! Great introduction to design principles and tools. The Figma tutorials were especially helpful for my projects.'),
(8, 9, 3, 'Basic Git course that covers the fundamentals. Good for absolute beginners but could include more advanced Git workflows and collaboration techniques.'),
(15, 9, 4, 'Good introduction to Git and GitHub. As a first-year student, this course gave me the foundation I needed for collaborative programming projects.');

-- =====================================================
-- ADMIN DATA (3 Admin Users)
-- =====================================================
-- Admin users for system management
INSERT INTO admin (username, password, role) VALUES
('admin', 'admin123', 'Super Admin'),
('course_manager', 'manager123', 'Course Manager'),
('moderator', 'mod123', 'Content Moderator');

-- =====================================================
-- DATA INSERTION COMPLETE
-- =====================================================

-- Display summary of inserted data
SELECT 'Sample Data Insertion Complete!' AS Status;

SELECT 
    (SELECT COUNT(*) FROM students) AS Students,
    (SELECT COUNT(*) FROM courses) AS Courses,
    (SELECT COUNT(*) FROM skills) AS Skills,
    (SELECT COUNT(*) FROM student_skills) AS Student_Skills,
    (SELECT COUNT(*) FROM course_skills) AS Course_Skills,
    (SELECT COUNT(*) FROM enrollments) AS Enrollments,
    (SELECT COUNT(*) FROM feedback) AS Feedback_Entries,
    (SELECT COUNT(*) FROM admin) AS Admin_Users;

-- Show some sample data
SELECT 'Recent Enrollments:' AS Info;
SELECT s.name AS Student, c.course_name AS Course, e.completion_status AS Status, e.enrollment_date
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id
ORDER BY e.enrollment_date DESC
LIMIT 5;

SELECT 'Top Rated Courses:' AS Info;
SELECT course_name, category, average_rating, total_enrollments
FROM courses
ORDER BY average_rating DESC, total_enrollments DESC
LIMIT 5;
