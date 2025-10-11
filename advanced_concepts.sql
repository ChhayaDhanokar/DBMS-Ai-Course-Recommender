-- =====================================================
-- AI COURSE RECOMMENDATION SYSTEM - ADVANCED CONCEPTS
-- =====================================================
-- DBMS Mini Project - Views, Triggers, and Stored Procedures
-- Author: Student
-- Date: October 2025
-- Description: Advanced database concepts demonstration
-- Includes: 3 Views, 3 Triggers, 3 Stored Procedures
-- =====================================================

-- =====================================================
-- SECTION 1: VIEWS
-- =====================================================

-- Drop existing views if they exist
DROP VIEW IF EXISTS top_courses;
DROP VIEW IF EXISTS student_enrollment_summary;
DROP VIEW IF EXISTS course_statistics;

-- VIEW 1: TOP_COURSES
-- Purpose: Display high-quality courses (rating >= 4.0) for easy access
-- Usage: SELECT * FROM top_courses; - Shows best courses for recommendations
CREATE VIEW top_courses AS
SELECT 
    course_id,
    course_name,
    category,
    difficulty_level,
    duration_hours,
    average_rating,
    total_enrollments,
    description,
    created_date
FROM courses
WHERE average_rating >= 4.0
ORDER BY average_rating DESC, total_enrollments DESC;

-- VIEW 2: STUDENT_ENROLLMENT_SUMMARY
-- Purpose: Comprehensive student statistics for dashboard and analytics
-- Usage: SELECT * FROM student_enrollment_summary WHERE student_id = 1;
CREATE VIEW student_enrollment_summary AS
SELECT 
    s.student_id,
    s.name AS student_name,
    s.email,
    s.department,
    s.year,
    COUNT(e.enrollment_id) AS total_courses,
    COUNT(CASE WHEN e.completion_status = 'Completed' THEN 1 END) AS completed_courses,
    COUNT(CASE WHEN e.completion_status = 'In Progress' THEN 1 END) AS in_progress_courses,
    COUNT(CASE WHEN e.completion_status = 'Enrolled' THEN 1 END) AS enrolled_courses,
    COUNT(CASE WHEN e.completion_status = 'Dropped' THEN 1 END) AS dropped_courses,
    ROUND(
        (COUNT(CASE WHEN e.completion_status = 'Completed' THEN 1 END) * 100.0) / 
        NULLIF(COUNT(e.enrollment_id), 0), 2
    ) AS completion_percentage,
    MAX(e.enrollment_date) AS last_enrollment_date,
    s.registration_date
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.name, s.email, s.department, s.year, s.registration_date;

-- VIEW 3: COURSE_STATISTICS
-- Purpose: Detailed course analytics including feedback statistics
-- Usage: SELECT * FROM course_statistics ORDER BY avg_feedback_rating DESC;
CREATE VIEW course_statistics AS
SELECT 
    c.course_id,
    c.course_name,
    c.category,
    c.difficulty_level,
    c.duration_hours,
    c.total_enrollments,
    c.average_rating AS stored_rating,
    COUNT(f.feedback_id) AS total_feedback_count,
    COALESCE(AVG(f.rating), 0) AS avg_feedback_rating,
    COUNT(CASE WHEN f.rating = 5 THEN 1 END) AS five_star_count,
    COUNT(CASE WHEN f.rating = 4 THEN 1 END) AS four_star_count,
    COUNT(CASE WHEN f.rating = 3 THEN 1 END) AS three_star_count,
    COUNT(CASE WHEN f.rating = 2 THEN 1 END) AS two_star_count,
    COUNT(CASE WHEN f.rating = 1 THEN 1 END) AS one_star_count,
    COUNT(DISTINCT e.student_id) AS unique_students_enrolled,
    COUNT(CASE WHEN e.completion_status = 'Completed' THEN 1 END) AS completed_enrollments,
    ROUND(
        (COUNT(CASE WHEN e.completion_status = 'Completed' THEN 1 END) * 100.0) / 
        NULLIF(COUNT(e.enrollment_id), 0), 2
    ) AS completion_rate,
    c.created_date
FROM courses c
LEFT JOIN feedback f ON c.course_id = f.course_id
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.category, c.difficulty_level, 
         c.duration_hours, c.total_enrollments, c.average_rating, c.created_date;

-- Test the views
SELECT 'Testing Views:' AS Info;
SELECT 'Top Courses View:' AS View_Name;
SELECT course_name, average_rating, total_enrollments FROM top_courses LIMIT 3;

SELECT 'Student Enrollment Summary View:' AS View_Name;
SELECT student_name, total_courses, completed_courses, completion_percentage 
FROM student_enrollment_summary LIMIT 3;

SELECT 'Course Statistics View:' AS View_Name;
SELECT course_name, total_feedback_count, avg_feedback_rating, completion_rate 
FROM course_statistics LIMIT 3;

-- =====================================================
-- SECTION 2: TRIGGERS
-- =====================================================

-- Change delimiter for trigger definitions
DELIMITER //

-- Drop existing triggers if they exist
DROP TRIGGER IF EXISTS update_course_rating//
DROP TRIGGER IF EXISTS update_enrollment_count//
DROP TRIGGER IF EXISTS prevent_course_deletion//

-- TRIGGER 1: UPDATE_COURSE_RATING
-- Purpose: Automatically recalculate and update course average rating when new feedback is added
-- Fires: AFTER INSERT on feedback table
-- Logic: Calculate new average from all feedback for the course and update courses table
CREATE TRIGGER update_course_rating
AFTER INSERT ON feedback
FOR EACH ROW
BEGIN
    DECLARE new_avg_rating DECIMAL(3,2);
    
    -- Calculate the new average rating for the course
    SELECT AVG(rating) INTO new_avg_rating
    FROM feedback
    WHERE course_id = NEW.course_id;
    
    -- Update the courses table with the new average rating
    UPDATE courses
    SET average_rating = new_avg_rating
    WHERE course_id = NEW.course_id;
    
    -- Log the update (optional - for debugging)
    INSERT INTO temp_trigger_log (trigger_name, action, course_id, old_rating, new_rating, timestamp)
    VALUES ('update_course_rating', 'UPDATE', NEW.course_id, 
            (SELECT average_rating FROM courses WHERE course_id = NEW.course_id), 
            new_avg_rating, NOW())
    ON DUPLICATE KEY UPDATE timestamp = NOW();
    
END//

-- TRIGGER 2: UPDATE_ENROLLMENT_COUNT
-- Purpose: Automatically increment course enrollment count when student enrolls
-- Fires: AFTER INSERT on enrollments table
-- Logic: Increment total_enrollments counter in courses table
CREATE TRIGGER update_enrollment_count
AFTER INSERT ON enrollments
FOR EACH ROW
BEGIN
    -- Increment the enrollment count for the course
    UPDATE courses
    SET total_enrollments = total_enrollments + 1
    WHERE course_id = NEW.course_id;
    
    -- Log the enrollment (optional - for analytics)
    INSERT INTO temp_trigger_log (trigger_name, action, course_id, student_id, timestamp)
    VALUES ('update_enrollment_count', 'INCREMENT', NEW.course_id, NEW.student_id, NOW())
    ON DUPLICATE KEY UPDATE timestamp = NOW();
    
END//

-- TRIGGER 3: PREVENT_COURSE_DELETION
-- Purpose: Prevent deletion of courses that have active (non-completed) enrollments
-- Fires: BEFORE DELETE on courses table
-- Logic: Check for active enrollments and raise error if found
CREATE TRIGGER prevent_course_deletion
BEFORE DELETE ON courses
FOR EACH ROW
BEGIN
    DECLARE active_enrollments INT DEFAULT 0;
    DECLARE error_message VARCHAR(255);
    
    -- Count active enrollments (not completed or dropped)
    SELECT COUNT(*) INTO active_enrollments
    FROM enrollments
    WHERE course_id = OLD.course_id
    AND completion_status IN ('Enrolled', 'In Progress');
    
    -- If there are active enrollments, prevent deletion
    IF active_enrollments > 0 THEN
        SET error_message = CONCAT('Cannot delete course "', OLD.course_name, 
                                 '". It has ', active_enrollments, ' active enrollment(s).');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
    END IF;
    
    -- Log the deletion attempt
    INSERT INTO temp_trigger_log (trigger_name, action, course_id, message, timestamp)
    VALUES ('prevent_course_deletion', 'DELETE_ATTEMPT', OLD.course_id, 
            CASE WHEN active_enrollments > 0 THEN 'BLOCKED' ELSE 'ALLOWED' END, NOW())
    ON DUPLICATE KEY UPDATE timestamp = NOW();
    
END//

-- Reset delimiter
DELIMITER ;

-- Create temporary log table for trigger testing (optional)
CREATE TABLE IF NOT EXISTS temp_trigger_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    trigger_name VARCHAR(50),
    action VARCHAR(20),
    course_id INT,
    student_id INT DEFAULT NULL,
    old_rating DECIMAL(3,2) DEFAULT NULL,
    new_rating DECIMAL(3,2) DEFAULT NULL,
    message VARCHAR(255) DEFAULT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_log (trigger_name, course_id, student_id, timestamp)
);

-- Test the triggers
SELECT 'Testing Triggers:' AS Info;

-- Test trigger 1: Insert feedback and see rating update
INSERT INTO feedback (student_id, course_id, rating, review_text)
VALUES (1, 1, 5, 'Testing trigger - excellent course!');

SELECT 'After feedback insert - Course rating updated:' AS Test;
SELECT course_name, average_rating FROM courses WHERE course_id = 1;

-- Test trigger 2: Insert enrollment and see count update
INSERT INTO enrollments (student_id, course_id, completion_status)
VALUES (2, 2, 'Enrolled');

SELECT 'After enrollment insert - Enrollment count updated:' AS Test;
SELECT course_name, total_enrollments FROM courses WHERE course_id = 2;

-- =====================================================
-- SECTION 3: STORED PROCEDURES
-- =====================================================

-- Change delimiter for procedure definitions
DELIMITER //

-- Drop existing procedures if they exist
DROP PROCEDURE IF EXISTS get_recommendations//
DROP PROCEDURE IF EXISTS enroll_student//
DROP PROCEDURE IF EXISTS get_student_dashboard//

-- STORED PROCEDURE 1: GET_RECOMMENDATIONS
-- Purpose: Get personalized course recommendations based on student's skills
-- Input: student_id
-- Output: Top 5 recommended courses that student hasn't enrolled in
-- Logic: Match student skills with course requirements, exclude enrolled courses
CREATE PROCEDURE get_recommendations(IN input_student_id INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    -- Validate input
    IF input_student_id IS NULL OR input_student_id <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid student ID provided';
    END IF;
    
    -- Check if student exists
    IF NOT EXISTS (SELECT 1 FROM students WHERE student_id = input_student_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student not found';
    END IF;
    
    -- Get recommendations based on student's skills
    SELECT DISTINCT
        c.course_id,
        c.course_name,
        c.category,
        c.difficulty_level,
        c.duration_hours,
        c.average_rating,
        c.total_enrollments,
        c.description,
        COUNT(DISTINCT cs.skill_id) AS matching_skills,
        ROUND(
            (COUNT(DISTINCT cs.skill_id) * 100.0) / 
            (SELECT COUNT(*) FROM course_skills WHERE course_id = c.course_id), 2
        ) AS skill_match_percentage
    FROM courses c
    INNER JOIN course_skills cs ON c.course_id = cs.course_id
    INNER JOIN student_skills ss ON cs.skill_id = ss.skill_id
    WHERE ss.student_id = input_student_id
    AND c.course_id NOT IN (
        -- Exclude courses already enrolled by the student
        SELECT course_id FROM enrollments WHERE student_id = input_student_id
    )
    GROUP BY c.course_id, c.course_name, c.category, c.difficulty_level, 
             c.duration_hours, c.average_rating, c.total_enrollments, c.description
    ORDER BY skill_match_percentage DESC, c.average_rating DESC, c.total_enrollments DESC
    LIMIT 5;
    
END//

-- STORED PROCEDURE 2: ENROLL_STUDENT
-- Purpose: Handle student enrollment with proper transaction management
-- Input: student_id, course_id
-- Output: Success/failure message with enrollment details
-- Logic: Insert enrollment, update course count, handle duplicates and errors
CREATE PROCEDURE enroll_student(
    IN input_student_id INT, 
    IN input_course_id INT,
    OUT result_message VARCHAR(255),
    OUT enrollment_id INT
)
BEGIN
    DECLARE student_exists INT DEFAULT 0;
    DECLARE course_exists INT DEFAULT 0;
    DECLARE already_enrolled INT DEFAULT 0;
    DECLARE course_name_var VARCHAR(200);
    DECLARE student_name_var VARCHAR(100);
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET result_message = 'Error: Enrollment failed due to database error';
        SET enrollment_id = -1;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Validate inputs
    IF input_student_id IS NULL OR input_student_id <= 0 THEN
        SET result_message = 'Error: Invalid student ID';
        SET enrollment_id = -1;
        ROLLBACK;
    ELSEIF input_course_id IS NULL OR input_course_id <= 0 THEN
        SET result_message = 'Error: Invalid course ID';
        SET enrollment_id = -1;
        ROLLBACK;
    ELSE
        -- Check if student exists
        SELECT COUNT(*), name INTO student_exists, student_name_var
        FROM students WHERE student_id = input_student_id;
        
        -- Check if course exists
        SELECT COUNT(*), course_name INTO course_exists, course_name_var
        FROM courses WHERE course_id = input_course_id;
        
        -- Check if already enrolled
        SELECT COUNT(*) INTO already_enrolled
        FROM enrollments 
        WHERE student_id = input_student_id AND course_id = input_course_id;
        
        IF student_exists = 0 THEN
            SET result_message = 'Error: Student not found';
            SET enrollment_id = -1;
            ROLLBACK;
        ELSEIF course_exists = 0 THEN
            SET result_message = 'Error: Course not found';
            SET enrollment_id = -1;
            ROLLBACK;
        ELSEIF already_enrolled > 0 THEN
            SET result_message = CONCAT('Error: Student already enrolled in course "', course_name_var, '"');
            SET enrollment_id = -1;
            ROLLBACK;
        ELSE
            -- Perform enrollment
            INSERT INTO enrollments (student_id, course_id, completion_status, enrollment_date)
            VALUES (input_student_id, input_course_id, 'Enrolled', NOW());
            
            SET enrollment_id = LAST_INSERT_ID();
            
            -- Update course enrollment count (this will also trigger the update_enrollment_count trigger)
            -- Note: The trigger will also increment, so we don't need to do it manually
            
            SET result_message = CONCAT('Success: ', student_name_var, ' enrolled in "', course_name_var, '"');
            
            COMMIT;
        END IF;
    END IF;
    
END//

-- STORED PROCEDURE 3: GET_STUDENT_DASHBOARD
-- Purpose: Retrieve comprehensive student dashboard data in one call
-- Input: student_id
-- Output: Student details, enrollment statistics, recent activities
-- Logic: Join multiple tables to get complete student overview
CREATE PROCEDURE get_student_dashboard(IN input_student_id INT)
BEGIN
    DECLARE student_exists INT DEFAULT 0;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        RESIGNAL;
    END;
    
    -- Validate input
    IF input_student_id IS NULL OR input_student_id <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid student ID provided';
    END IF;
    
    -- Check if student exists
    SELECT COUNT(*) INTO student_exists FROM students WHERE student_id = input_student_id;
    
    IF student_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student not found';
    END IF;
    
    -- Return student basic information and statistics
    SELECT 
        s.student_id,
        s.name,
        s.email,
        s.department,
        s.year,
        s.registration_date,
        ses.total_courses,
        ses.completed_courses,
        ses.in_progress_courses,
        ses.enrolled_courses,
        ses.completion_percentage,
        ses.last_enrollment_date
    FROM students s
    LEFT JOIN student_enrollment_summary ses ON s.student_id = ses.student_id
    WHERE s.student_id = input_student_id;
    
    -- Return student's current enrollments with course details
    SELECT 
        e.enrollment_id,
        c.course_name,
        c.category,
        c.difficulty_level,
        c.duration_hours,
        c.average_rating,
        e.completion_status,
        e.enrollment_date,
        e.completion_date,
        CASE 
            WHEN e.completion_status = 'Completed' THEN 'Course completed successfully'
            WHEN e.completion_status = 'In Progress' THEN 'Currently learning'
            WHEN e.completion_status = 'Enrolled' THEN 'Ready to start'
            WHEN e.completion_status = 'Dropped' THEN 'Course dropped'
            ELSE 'Unknown status'
        END AS status_description
    FROM enrollments e
    INNER JOIN courses c ON e.course_id = c.course_id
    WHERE e.student_id = input_student_id
    ORDER BY e.enrollment_date DESC;
    
    -- Return student's skills
    SELECT 
        sk.skill_name,
        sk.category,
        ss.proficiency_level,
        ss.added_date
    FROM student_skills ss
    INNER JOIN skills sk ON ss.skill_id = sk.skill_id
    WHERE ss.student_id = input_student_id
    ORDER BY ss.proficiency_level DESC, sk.skill_name;
    
    -- Return student's feedback history
    SELECT 
        c.course_name,
        f.rating,
        f.review_text,
        f.feedback_date
    FROM feedback f
    INNER JOIN courses c ON f.course_id = c.course_id
    WHERE f.student_id = input_student_id
    ORDER BY f.feedback_date DESC;
    
END//

-- Reset delimiter
DELIMITER ;

-- =====================================================
-- TESTING STORED PROCEDURES
-- =====================================================

SELECT 'Testing Stored Procedures:' AS Info;

-- Test Procedure 1: Get recommendations for student ID 1
SELECT 'Recommendations for Student ID 1:' AS Test;
CALL get_recommendations(1);

-- Test Procedure 2: Enroll student (with error handling)
SELECT 'Testing Student Enrollment:' AS Test;
CALL enroll_student(3, 5, @result_msg, @enroll_id);
SELECT @result_msg AS enrollment_result, @enroll_id AS new_enrollment_id;

-- Test Procedure 3: Get student dashboard
SELECT 'Student Dashboard for Student ID 1:' AS Test;
CALL get_student_dashboard(1);

-- =====================================================
-- DEMONSTRATION QUERIES
-- =====================================================

-- Show how views simplify complex queries
SELECT 'Using Views for Easy Data Access:' AS Demo;

-- Get top courses easily
SELECT course_name, average_rating FROM top_courses LIMIT 3;

-- Get student statistics easily
SELECT student_name, completion_percentage FROM student_enrollment_summary 
WHERE completion_percentage > 50 LIMIT 3;

-- Get course analytics easily
SELECT course_name, completion_rate, avg_feedback_rating FROM course_statistics 
ORDER BY completion_rate DESC LIMIT 3;

-- =====================================================
-- CLEANUP SECTION (Optional)
-- =====================================================

-- Uncomment the following lines if you want to clean up test data
-- DELETE FROM temp_trigger_log;
-- DROP TABLE IF EXISTS temp_trigger_log;

-- =====================================================
-- SUMMARY REPORT
-- =====================================================

SELECT '=== ADVANCED CONCEPTS DEMONSTRATION COMPLETE ===' AS Summary;

SELECT 'Views Created:' AS Category, '3 Views (top_courses, student_enrollment_summary, course_statistics)' AS Details
UNION ALL
SELECT 'Triggers Created:', '3 Triggers (rating update, enrollment count, deletion prevention)'
UNION ALL
SELECT 'Stored Procedures:', '3 Procedures (recommendations, enrollment, dashboard)'
UNION ALL
SELECT 'Features Demonstrated:', 'Complex JOINs, Aggregations, Transactions, Error Handling'
UNION ALL
SELECT 'Business Logic:', 'Automatic updates, Data integrity, User experience optimization';

-- Show current view data
SELECT 'Current System Statistics:' AS Info;
SELECT 
    (SELECT COUNT(*) FROM top_courses) AS high_rated_courses,
    (SELECT COUNT(*) FROM student_enrollment_summary WHERE total_courses > 0) AS active_students,
    (SELECT AVG(completion_rate) FROM course_statistics) AS avg_completion_rate;

-- =====================================================
-- END OF ADVANCED CONCEPTS DEMONSTRATION
-- =====================================================





