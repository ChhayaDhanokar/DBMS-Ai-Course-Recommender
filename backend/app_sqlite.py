# =====================================================
# AI COURSE RECOMMENDATION SYSTEM - SQLITE VERSION
# =====================================================
# Flask application with SQLite database
# Author: Student
# Date: October 2025
# Description: Complete working system using SQLite
# =====================================================

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app, supports_credentials=True)

# Database file path
DB_PATH = 'course_recommendation.db'

def init_database():
    """Initialize SQLite database with tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            department TEXT,
            year TEXT,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            duration_hours INTEGER,
            difficulty_level TEXT CHECK(difficulty_level IN ('Beginner', 'Intermediate', 'Advanced')),
            average_rating REAL DEFAULT 0.0,
            total_enrollments INTEGER DEFAULT 0,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT UNIQUE NOT NULL,
            category TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_skills (
            student_id INTEGER,
            skill_id INTEGER,
            proficiency_level TEXT CHECK(proficiency_level IN ('Beginner', 'Intermediate', 'Advanced')),
            added_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (student_id, skill_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course_skills (
            course_id INTEGER,
            skill_id INTEGER,
            PRIMARY KEY (course_id, skill_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            completion_status TEXT DEFAULT 'Enrolled' CHECK(completion_status IN ('Enrolled', 'In Progress', 'Completed', 'Dropped')),
            completion_date DATETIME,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            review_text TEXT,
            feedback_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def populate_sample_data():
    """Populate database with sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM students')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Insert sample students
    students = [
        ('Arjun Sharma', 'arjun.sharma@college.edu', hash_password('password123'), '9876543210', 'Computer Science', '3rd Year'),
        ('Priya Patel', 'priya.patel@college.edu', hash_password('password123'), '9876543211', 'Information Technology', '2nd Year'),
        ('Rajesh Kumar', 'rajesh.kumar@college.edu', hash_password('password123'), '9876543212', 'Electronics', '4th Year'),
        ('Sneha Singh', 'sneha.singh@college.edu', hash_password('password123'), '9876543213', 'Computer Science', '1st Year'),
        ('Amit Verma', 'amit.verma@college.edu', hash_password('password123'), '9876543214', 'Information Technology', '3rd Year')
    ]
    
    cursor.executemany('''
        INSERT INTO students (name, email, password, phone, department, year)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', students)
    
    # Insert sample skills
    skills = [
        ('Python Programming', 'Programming'),
        ('JavaScript', 'Programming'),
        ('SQL', 'Database'),
        ('React', 'Web Development'),
        ('Machine Learning', 'AI/ML'),
        ('Data Analysis', 'Data Science'),
        ('HTML/CSS', 'Web Development'),
        ('Docker', 'DevOps'),
        ('UI Design', 'Design'),
        ('Node.js', 'Programming')
    ]
    
    cursor.executemany('''
        INSERT INTO skills (skill_name, category)
        VALUES (?, ?)
    ''', skills)
    
    # Insert sample courses
    courses = [
        ('Complete Python Bootcamp', 'Learn Python from scratch to advanced level', 'Programming', 40, 'Beginner'),
        ('React Development Course', 'Build modern web applications with React', 'Web Development', 30, 'Intermediate'),
        ('Machine Learning Fundamentals', 'Introduction to ML algorithms and techniques', 'AI/ML', 50, 'Advanced'),
        ('SQL Mastery', 'Database design and query optimization', 'Database', 25, 'Intermediate'),
        ('Data Science with Python', 'Analyze data using Python libraries', 'Data Science', 45, 'Intermediate'),
        ('Docker for Developers', 'Containerization and deployment strategies', 'DevOps', 20, 'Intermediate'),
        ('UI/UX Design Principles', 'Create beautiful and functional interfaces', 'Design', 35, 'Beginner'),
        ('Node.js Backend Development', 'Build scalable server applications', 'Programming', 40, 'Advanced')
    ]
    
    cursor.executemany('''
        INSERT INTO courses (course_name, description, category, duration_hours, difficulty_level)
        VALUES (?, ?, ?, ?, ?)
    ''', courses)
    
    # Insert student skills
    student_skills = [
        (1, 1, 'Advanced'),  # Arjun - Python Advanced
        (1, 3, 'Intermediate'),  # Arjun - SQL Intermediate
        (1, 5, 'Beginner'),  # Arjun - ML Beginner
        (2, 2, 'Intermediate'),  # Priya - JavaScript Intermediate
        (2, 4, 'Intermediate'),  # Priya - React Intermediate
        (2, 7, 'Advanced'),  # Priya - HTML/CSS Advanced
        (3, 1, 'Intermediate'),  # Rajesh - Python Intermediate
        (3, 6, 'Advanced'),  # Rajesh - Data Analysis Advanced
        (4, 1, 'Beginner'),  # Sneha - Python Beginner
        (4, 7, 'Intermediate'),  # Sneha - HTML/CSS Intermediate
        (5, 2, 'Advanced'),  # Amit - JavaScript Advanced
        (5, 8, 'Intermediate'),  # Amit - Docker Intermediate
    ]
    
    cursor.executemany('''
        INSERT INTO student_skills (student_id, skill_id, proficiency_level)
        VALUES (?, ?, ?)
    ''', student_skills)
    
    # Insert course skills
    course_skills = [
        (1, 1),  # Python Course - Python skill
        (2, 2),  # React Course - JavaScript skill
        (2, 4),  # React Course - React skill
        (3, 1),  # ML Course - Python skill
        (3, 5),  # ML Course - ML skill
        (4, 3),  # SQL Course - SQL skill
        (5, 1),  # Data Science - Python skill
        (5, 6),  # Data Science - Data Analysis skill
        (6, 8),  # Docker Course - Docker skill
        (7, 7),  # UI Design - HTML/CSS skill
        (7, 9),  # UI Design - UI Design skill
        (8, 2),  # Node.js - JavaScript skill
    ]
    
    cursor.executemany('''
        INSERT INTO course_skills (course_id, skill_id)
        VALUES (?, ?)
    ''', course_skills)
    
    # Insert sample enrollments
    enrollments = [
        (1, 1, 'Completed', '2024-01-15'),
        (1, 3, 'In Progress', None),
        (2, 2, 'Completed', '2024-02-10'),
        (2, 7, 'Enrolled', None),
        (3, 4, 'Completed', '2024-01-20'),
        (3, 5, 'In Progress', None),
        (4, 1, 'Enrolled', None),
        (5, 2, 'Completed', '2024-02-05'),
        (5, 8, 'Enrolled', None)
    ]
    
    cursor.executemany('''
        INSERT INTO enrollments (student_id, course_id, completion_status, completion_date)
        VALUES (?, ?, ?, ?)
    ''', enrollments)
    
    # Insert sample feedback
    feedback = [
        (1, 1, 5, 'Excellent course! Very well structured and easy to follow.'),
        (2, 2, 4, 'Great content, learned a lot about React development.'),
        (3, 4, 5, 'Perfect for learning SQL fundamentals.'),
        (5, 2, 4, 'Good course, would recommend to others.')
    ]
    
    cursor.executemany('''
        INSERT INTO feedback (student_id, course_id, rating, review_text)
        VALUES (?, ?, ?, ?)
    ''', feedback)
    
    # Update course ratings and enrollment counts
    cursor.execute('''
        UPDATE courses SET average_rating = (
            SELECT AVG(rating) FROM feedback WHERE course_id = courses.course_id
        )
    ''')
    
    cursor.execute('''
        UPDATE courses SET total_enrollments = (
            SELECT COUNT(*) FROM enrollments WHERE course_id = courses.course_id
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()
populate_sample_data()

# =====================================================
# API ROUTES
# =====================================================

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'AI Course Recommendation API',
        'status': 'running',
        'version': '1.0.0',
        'description': 'DBMS Mini Project - Course Recommendation System'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# Authentication routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Student login"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT student_id, name, email, department, year
            FROM students 
            WHERE email = ? AND password = ?
        ''', (email, hash_password(password)))
        
        student = cursor.fetchone()
        conn.close()
        
        if student:
            session['user_id'] = student['student_id']
            session['user_type'] = 'student'
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'data': {
                    'student_id': student['student_id'],
                    'name': student['name'],
                    'email': student['email'],
                    'department': student['department'],
                    'year': student['year']
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Student registration"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'password', 'phone', 'department', 'year']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute('SELECT student_id FROM students WHERE email = ?', (data['email'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Insert new student
        cursor.execute('''
            INSERT INTO students (name, email, password, phone, department, year)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['email'], hash_password(data['password']), 
              data['phone'], data['department'], data['year']))
        
        student_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'data': {
                'student_id': student_id,
                'name': data['name'],
                'email': data['email']
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Student logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# Courses routes
@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Get all courses with optional filters"""
    try:
        category = request.args.get('category')
        difficulty = request.args.get('difficulty_level')
        search = request.args.get('search')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM courses WHERE 1=1'
        params = []
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        if difficulty:
            query += ' AND difficulty_level = ?'
            params.append(difficulty)
        
        if search:
            query += ' AND (course_name LIKE ? OR description LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += ' ORDER BY average_rating DESC, total_enrollments DESC'
        
        cursor.execute(query, params)
        courses = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'courses': [dict(course) for course in courses],
                'categories': list(set([course['category'] for course in courses]))
            }
        })
        
    except Exception as e:
        logger.error(f"Get courses error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get single course details"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM courses WHERE course_id = ?', (course_id,))
        course = cursor.fetchone()
        
        if not course:
            conn.close()
            return jsonify({'success': False, 'message': 'Course not found'}), 404
        
        # Get required skills
        cursor.execute('''
            SELECT s.skill_name, s.category
            FROM skills s
            JOIN course_skills cs ON s.skill_id = cs.skill_id
            WHERE cs.course_id = ?
        ''', (course_id,))
        skills = cursor.fetchall()
        
        conn.close()
        
        course_data = dict(course)
        course_data['required_skills'] = [dict(skill) for skill in skills]
        
        return jsonify({
            'success': True,
            'data': course_data
        })
        
    except Exception as e:
        logger.error(f"Get course error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

# Recommendations route
@app.route('/api/recommendations/<int:student_id>', methods=['GET'])
def get_recommendations(student_id):
    """Get personalized recommendations"""
    try:
        limit = request.args.get('limit', 5, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get student's skills
        cursor.execute('''
            SELECT s.skill_id, s.skill_name, ss.proficiency_level
            FROM skills s
            JOIN student_skills ss ON s.skill_id = ss.skill_id
            WHERE ss.student_id = ?
        ''', (student_id,))
        student_skills = cursor.fetchall()
        
        if not student_skills:
            conn.close()
            return jsonify({
                'success': True,
                'data': {
                    'recommendations': [],
                    'message': 'Add skills to your profile to get recommendations'
                }
            })
        
        student_skill_ids = [skill['skill_id'] for skill in student_skills]
        
        # Get courses with matching skills (excluding already enrolled)
        cursor.execute('''
            SELECT DISTINCT c.*, 
                   COUNT(cs.skill_id) as matching_skills,
                   (COUNT(cs.skill_id) * 1.0 / total_skills.total) as skill_match_ratio
            FROM courses c
            JOIN course_skills cs ON c.course_id = cs.course_id
            JOIN (
                SELECT course_id, COUNT(*) as total 
                FROM course_skills 
                GROUP BY course_id
            ) total_skills ON c.course_id = total_skills.course_id
            WHERE cs.skill_id IN ({})
            AND c.course_id NOT IN (
                SELECT course_id FROM enrollments WHERE student_id = ?
            )
            GROUP BY c.course_id
            ORDER BY skill_match_ratio DESC, c.average_rating DESC
            LIMIT ?
        '''.format(','.join('?' * len(student_skill_ids))), 
        student_skill_ids + [student_id, limit])
        
        recommendations = cursor.fetchall()
        conn.close()
        
        # Calculate match scores
        for rec in recommendations:
            rec['match_score'] = min(100, (rec['skill_match_ratio'] * 60) + (rec['average_rating'] * 8))
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': [dict(rec) for rec in recommendations]
            }
        })
        
    except Exception as e:
        logger.error(f"Get recommendations error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

# Enrollments route
@app.route('/api/enrollments', methods=['POST'])
def create_enrollment():
    """Enroll student in course"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        
        if not student_id or not course_id:
            return jsonify({'success': False, 'message': 'Student ID and Course ID required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if already enrolled
        cursor.execute('''
            SELECT enrollment_id FROM enrollments 
            WHERE student_id = ? AND course_id = ?
        ''', (student_id, course_id))
        
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Already enrolled in this course'}), 400
        
        # Create enrollment
        cursor.execute('''
            INSERT INTO enrollments (student_id, course_id)
            VALUES (?, ?)
        ''', (student_id, course_id))
        
        # Update course enrollment count
        cursor.execute('''
            UPDATE courses 
            SET total_enrollments = (
                SELECT COUNT(*) FROM enrollments WHERE course_id = ?
            )
            WHERE course_id = ?
        ''', (course_id, course_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Successfully enrolled in course'
        }), 201
        
    except Exception as e:
        logger.error(f"Create enrollment error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/enrollments/student/<int:student_id>', methods=['GET'])
def get_enrollments(student_id):
    """Get student enrollments"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.*, c.course_name, c.description, c.category, c.duration_hours,
                   c.difficulty_level, c.average_rating, c.total_enrollments
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.student_id = ?
            ORDER BY e.enrollment_date DESC
        ''', (student_id,))
        
        enrollments = cursor.fetchall()
        conn.close()
        
        # Calculate statistics
        total = len(enrollments)
        completed = len([e for e in enrollments if e['completion_status'] == 'Completed'])
        in_progress = len([e for e in enrollments if e['completion_status'] == 'In Progress'])
        enrolled = len([e for e in enrollments if e['completion_status'] == 'Enrolled'])
        
        return jsonify({
            'success': True,
            'data': {
                'enrollments': [dict(e) for e in enrollments],
                'statistics': {
                    'total_enrollments': total,
                    'completed_count': completed,
                    'in_progress_count': in_progress,
                    'enrolled_count': enrolled,
                    'completion_rate': round((completed / total * 100), 1) if total > 0 else 0
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Get enrollments error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

# Skills routes
@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM skills ORDER BY skill_name')
        skills = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'skills': [dict(skill) for skill in skills]
            }
        })
        
    except Exception as e:
        logger.error(f"Get skills error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/skills/student/<int:student_id>', methods=['GET'])
def get_student_skills(student_id):
    """Get student skills"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.*, ss.proficiency_level, ss.added_date
            FROM skills s
            JOIN student_skills ss ON s.skill_id = ss.skill_id
            WHERE ss.student_id = ?
            ORDER BY ss.added_date DESC
        ''', (student_id,))
        
        skills = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'skills': [dict(skill) for skill in skills]
            }
        })
        
    except Exception as e:
        logger.error(f"Get student skills error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

# Feedback routes
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit course feedback"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        rating = data.get('rating')
        review_text = data.get('review_text')
        
        if not all([student_id, course_id, rating]):
            return jsonify({'success': False, 'message': 'Student ID, Course ID, and rating required'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if feedback already exists
        cursor.execute('''
            SELECT feedback_id FROM feedback 
            WHERE student_id = ? AND course_id = ?
        ''', (student_id, course_id))
        
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Feedback already submitted for this course'}), 400
        
        # Insert feedback
        cursor.execute('''
            INSERT INTO feedback (student_id, course_id, rating, review_text)
            VALUES (?, ?, ?, ?)
        ''', (student_id, course_id, rating, review_text))
        
        # Update course rating
        cursor.execute('''
            UPDATE courses 
            SET average_rating = (
                SELECT AVG(rating) FROM feedback WHERE course_id = ?
            )
            WHERE course_id = ?
        ''', (course_id, course_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Submit feedback error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/feedback/course/<int:course_id>', methods=['GET'])
def get_course_feedback(course_id):
    """Get course feedback"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.*, s.name as student_name, s.department
            FROM feedback f
            JOIN students s ON f.student_id = s.student_id
            WHERE f.course_id = ?
            ORDER BY f.feedback_date DESC
        ''', (course_id,))
        
        feedback = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'feedback': [dict(f) for f in feedback]
            }
        })
        
    except Exception as e:
        logger.error(f"Get course feedback error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Course Recommendation System...")
    print("📊 Database initialized with sample data")
    print("🌐 Server running at: http://localhost:5000")
    print("👤 Test login: arjun.sharma@college.edu / password123")
    app.run(debug=True, host='0.0.0.0', port=5000)




