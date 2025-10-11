# =====================================================
# AI COURSE RECOMMENDATION SYSTEM - STREAMLIT VERSION
# =====================================================
# DBMS Mini Project - Streamlit Frontend
# Author: Student
# Date: October 2025
# Description: Complete course recommendation system with Streamlit UI
# Database: SQLite with same schema and relationships
# =====================================================

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import hashlib
import json
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_PATH = 'backend/course_recommendation.db'

# AI Course platforms with real course links
COURSE_PLATFORMS = {
    'Machine Learning': [
        {'platform': 'Coursera', 'name': 'Machine Learning by Andrew Ng', 'url': 'https://www.coursera.org/learn/machine-learning', 'badge': 'badge-coursera'},
        {'platform': 'Udacity', 'name': 'Machine Learning Engineer', 'url': 'https://www.udacity.com/course/machine-learning-engineer-nanodegree--nd009t', 'badge': 'badge-udacity'},
        {'platform': 'edX', 'name': 'Deep Learning Fundamentals', 'url': 'https://www.edx.org/learn/deep-learning', 'badge': 'badge-edx'},
        {'platform': 'Udemy', 'name': 'Complete Machine Learning Bootcamp', 'url': 'https://www.udemy.com/course/complete-machine-learning-and-data-science-zero-to-mastery/', 'badge': 'badge-udemy'},
    ],
    'Deep Learning': [
        {'platform': 'Coursera', 'name': 'Deep Learning Specialization', 'url': 'https://www.coursera.org/specializations/deep-learning', 'badge': 'badge-coursera'},
        {'platform': 'Udacity', 'name': 'Deep Learning Nanodegree', 'url': 'https://www.udacity.com/course/deep-learning-nanodegree--nd101', 'badge': 'badge-udacity'},
        {'platform': 'Fast.ai', 'name': 'Practical Deep Learning', 'url': 'https://course.fast.ai/', 'badge': 'badge-edx'},
        {'platform': 'Udemy', 'name': 'Deep Learning A-Z', 'url': 'https://www.udemy.com/course/deeplearning/', 'badge': 'badge-udemy'},
    ],
    'Natural Language Processing': [
        {'platform': 'Coursera', 'name': 'Natural Language Processing', 'url': 'https://www.coursera.org/specializations/natural-language-processing', 'badge': 'badge-coursera'},
        {'platform': 'Udacity', 'name': 'Natural Language Processing', 'url': 'https://www.udacity.com/course/natural-language-processing-nanodegree--nd892', 'badge': 'badge-udacity'},
        {'platform': 'edX', 'name': 'NLP with Python', 'url': 'https://www.edx.org/learn/natural-language-processing', 'badge': 'badge-edx'},
        {'platform': 'Udemy', 'name': 'NLP with Deep Learning', 'url': 'https://www.udemy.com/course/natural-language-processing-with-deep-learning-in-python/', 'badge': 'badge-udemy'},
    ],
    'Computer Vision': [
        {'platform': 'Coursera', 'name': 'Computer Vision Basics', 'url': 'https://www.coursera.org/learn/computer-vision-basics', 'badge': 'badge-coursera'},
        {'platform': 'Udacity', 'name': 'Computer Vision Nanodegree', 'url': 'https://www.udacity.com/course/computer-vision-nanodegree--nd891', 'badge': 'badge-udacity'},
        {'platform': 'edX', 'name': 'Computer Vision Fundamentals', 'url': 'https://www.edx.org/learn/computer-vision', 'badge': 'badge-edx'},
        {'platform': 'Udemy', 'name': 'Computer Vision with OpenCV', 'url': 'https://www.udemy.com/course/python-for-computer-vision-with-opencv-and-deep-learning/', 'badge': 'badge-udemy'},
    ],
    'AI for Business': [
        {'platform': 'Coursera', 'name': 'AI for Business', 'url': 'https://www.coursera.org/specializations/ai-for-business', 'badge': 'badge-coursera'},
        {'platform': 'LinkedIn Learning', 'name': 'AI for Business Leaders', 'url': 'https://www.linkedin.com/learning/paths/ai-for-business-leaders', 'badge': 'badge-linkedin'},
        {'platform': 'edX', 'name': 'AI Strategy', 'url': 'https://www.edx.org/learn/artificial-intelligence', 'badge': 'badge-edx'},
        {'platform': 'Udemy', 'name': 'AI for Business Strategy', 'url': 'https://www.udemy.com/course/artificial-intelligence-for-business/', 'badge': 'badge-udemy'},
    ],
    'Robotics & AI': [
        {'platform': 'Coursera', 'name': 'Robotics Specialization', 'url': 'https://www.coursera.org/specializations/robotics', 'badge': 'badge-coursera'},
        {'platform': 'Udacity', 'name': 'Robotics Software Engineer', 'url': 'https://www.udacity.com/course/robotics-software-engineer--nd209', 'badge': 'badge-udacity'},
        {'platform': 'edX', 'name': 'Autonomous Systems', 'url': 'https://www.edx.org/learn/robotics', 'badge': 'badge-edx'},
        {'platform': 'Udemy', 'name': 'AI & Robotics with Python', 'url': 'https://www.udemy.com/course/artificial-intelligence-robotics-with-python/', 'badge': 'badge-udemy'},
    ],
    'AI Ethics & Governance': [
        {'platform': 'Coursera', 'name': 'AI Ethics', 'url': 'https://www.coursera.org/learn/ai-ethics', 'badge': 'badge-coursera'},
        {'platform': 'edX', 'name': 'Ethics of AI', 'url': 'https://www.edx.org/learn/artificial-intelligence-ethics', 'badge': 'badge-edx'},
        {'platform': 'LinkedIn Learning', 'name': 'AI Ethics for Business', 'url': 'https://www.linkedin.com/learning/ai-ethics-for-business', 'badge': 'badge-linkedin'},
        {'platform': 'Udemy', 'name': 'AI Ethics & Bias', 'url': 'https://www.udemy.com/course/ai-ethics-and-bias/', 'badge': 'badge-udemy'},
    ],
    'AI Programming': [
        {'platform': 'Coursera', 'name': 'Python for AI & ML', 'url': 'https://www.coursera.org/specializations/python-3-programming', 'badge': 'badge-coursera'},
        {'platform': 'Udacity', 'name': 'AI Programming with Python', 'url': 'https://www.udacity.com/course/ai-programming-python-nanodegree--nd089', 'badge': 'badge-udacity'},
        {'platform': 'edX', 'name': 'Python for Data Science', 'url': 'https://www.edx.org/learn/python', 'badge': 'badge-edx'},
        {'platform': 'Udemy', 'name': 'Python for AI & Machine Learning', 'url': 'https://www.udemy.com/course/python-for-machine-learning-data-science-masterclass/', 'badge': 'badge-udemy'},
    ],
}

# AI-focused questionnaire for course recommendations
QUESTIONNAIRE = {
    'ai_interest': {
        'question': '🤖 Which AI domain interests you most?',
        'options': {
            'Machine Learning': ['Machine Learning', 'AI Programming'],
            'Deep Learning': ['Deep Learning', 'Machine Learning'],
            'Natural Language Processing': ['Natural Language Processing', 'AI Programming'],
            'Computer Vision': ['Computer Vision', 'Deep Learning'],
            'AI for Business': ['AI for Business', 'AI Ethics & Governance'],
            'Robotics & AI': ['Robotics & AI', 'Machine Learning'],
            'AI Ethics & Governance': ['AI Ethics & Governance', 'AI for Business'],
            'General AI Programming': ['AI Programming', 'Machine Learning'],
        }
    },
    'experience_level': {
        'question': '📊 What is your AI/Programming experience?',
        'options': {
            'Complete Beginner': 'Beginner',
            'Some Python Knowledge': 'Beginner',
            'Intermediate Programmer': 'Intermediate',
            'Advanced/AI Professional': 'Advanced',
        }
    },
    'career_goal': {
        'question': '🎯 What is your AI career goal?',
        'options': {
            'AI Research Scientist': ['Deep Learning', 'Machine Learning', 'AI Ethics & Governance'],
            'Machine Learning Engineer': ['Machine Learning', 'Deep Learning', 'AI Programming'],
            'Data Scientist': ['Machine Learning', 'Natural Language Processing', 'AI Programming'],
            'AI Product Manager': ['AI for Business', 'AI Ethics & Governance', 'Machine Learning'],
            'Computer Vision Engineer': ['Computer Vision', 'Deep Learning', 'AI Programming'],
            'NLP Engineer': ['Natural Language Processing', 'Machine Learning', 'AI Programming'],
            'Robotics Engineer': ['Robotics & AI', 'Machine Learning', 'Computer Vision'],
            'AI Consultant': ['AI for Business', 'AI Ethics & Governance', 'Machine Learning'],
        }
    },
    'time_commitment': {
        'question': '⏰ How much time can you dedicate weekly?',
        'options': {
            '1-3 hours': 'short',
            '4-7 hours': 'medium',
            '8-15 hours': 'long',
            '15+ hours (Full-time)': 'intensive',
        }
    },
    'learning_style': {
        'question': '🎓 What is your preferred learning approach?',
        'options': {
            'Hands-on Projects & Coding': 'practical',
            'Theoretical Foundations': 'theoretical',
            'Video Lectures with Exercises': 'structured',
            'Interactive AI Labs': 'interactive',
        }
    },
}

# Page configuration
st.set_page_config(
    page_title="AI Course Recommender",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for compact design - ORIGINAL THEME
st.markdown("""
<style>
    /* Compact content padding with cleaner design */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1200px !important;
    }
    
    /* Target specific Streamlit container class */
    .st-emotion-cache-zy6yx3 {
        width: 100% !important;
        padding: 1rem 1.5rem 2rem !important;
        max-width: 1200px !important;
        min-width: auto !important;
    }
    
    /* Clean up element container spacing */
    .st-emotion-cache-10p9htt {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 0.5rem !important;
        height: auto !important;
    }
    
    /* Better header spacing */
    .main h1, .main h2, .main h3 {
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
        text-align: center !important;
    }
    
    /* Center all Streamlit headers */
    [data-testid="stHeadingWithActionElements"] {
        text-align: center !important;
    }
    
    [data-testid="stHeadingWithActionElements"] h1,
    [data-testid="stHeadingWithActionElements"] h2,
    [data-testid="stHeadingWithActionElements"] h3 {
        text-align: center !important;
    }
    
    /* Improved sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        border-right: none !important;
        padding-top: 1rem !important;
        color: white !important;
    }
    
    /* Clean main header */
    .main-header {
        font-size: 2rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    /* Improved button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 0.3rem 0 !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(90deg, #764ba2, #667eea) !important;
    }
    
    /* Sidebar button styling */
    .css-1d391kg .stButton > button {
        margin: 0.2rem 0 !important;
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .css-1d391kg .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Clean metric display */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef) !important;
        border: 1px solid #dee2e6 !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        margin: 0.3rem 0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Dark, attractive card design - ORIGINAL */
    .card {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        border: 3px solid #3498db;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        color: white;
    }
    
    .card-header {
        font-size: 1.4rem;
        font-weight: bold;
        color: #3498db;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 3px solid #3498db;
        text-align: center;
    }
    
    .course-card {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        border: 2px solid #e74c3c;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        color: white;
    }
    
    .course-card:hover {
        border-color: #3498db;
        box-shadow: 0 4px 12px rgba(52,152,219,0.4);
        background: linear-gradient(135deg, #2d2d2d, #3a3a3a);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #8e44ad, #9b59b6);
        color: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 5px;
        border: none;
        box-shadow: 0 4px 8px rgba(142,68,173,0.4);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 10px;
        color: white;
    }
    
    .stat-label {
        font-size: 1rem;
        color: white;
        font-weight: 500;
    }
    
    /* Force text colors for dark theme */
    .course-card h3 {
        color: #3498db !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        margin-bottom: 8px !important;
    }
    
    .course-card h4 {
        color: #3498db !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        margin-bottom: 8px !important;
    }
    
    .course-card p {
        color: #ecf0f1 !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
    }
    
    /* Interactive Quiz Styling */
    .quiz-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        color: white;
    }
    
    .quiz-step {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .quiz-step:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    .quiz-option {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
    }
    
    .quiz-option:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: #fff;
        transform: scale(1.02);
    }
    
    .quiz-option.selected {
        background: rgba(255, 255, 255, 0.3);
        border-color: #fff;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
    }
    
    /* Platform badges */
    .platform-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 3px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .badge-udemy {
        background: linear-gradient(135deg, #ec5252 0%, #a33e3e 100%);
        color: white;
    }
    
    .badge-coursera {
        background: linear-gradient(135deg, #0056d2 0%, #003d99 100%);
        color: white;
    }
    
    .badge-edx {
        background: linear-gradient(135deg, #02262b 0%, #064f5e 100%);
        color: white;
    }
    
    .badge-udacity {
        background: linear-gradient(135deg, #02b3e4 0%, #0189b3 100%);
        color: white;
    }
    
    .badge-linkedin {
        background: linear-gradient(135deg, #0077b5 0%, #005885 100%);
        color: white;
    }
    
    .badge-pluralsight {
        background: linear-gradient(135deg, #f15b2a 0%, #c1451f 100%);
        color: white;
    }
    
    .badge-fastai {
        background: linear-gradient(135deg, #00a86b 0%, #007a4d 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Database query functions
def execute_query(query, params=None):
    """Execute a database query and return results"""
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return pd.DataFrame()

def execute_insert(query, params=None):
    """Execute INSERT/UPDATE/DELETE query"""
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return False

def get_dashboard_stats():
    """Get dashboard statistics - SAME SQL as original"""
    stats = {}
    
    # Total courses
    courses_df = execute_query("SELECT COUNT(*) as count FROM courses")
    stats['total_courses'] = courses_df['count'].iloc[0] if not courses_df.empty else 0
    
    # Total students
    students_df = execute_query("SELECT COUNT(*) as count FROM students")
    stats['total_students'] = students_df['count'].iloc[0] if not students_df.empty else 0
    
    # Total enrollments
    enrollments_df = execute_query("SELECT COUNT(*) as count FROM enrollments")
    stats['total_enrollments'] = enrollments_df['count'].iloc[0] if not enrollments_df.empty else 0
    
    # Total skills
    skills_df = execute_query("SELECT COUNT(*) as count FROM skills")
    stats['total_skills'] = skills_df['count'].iloc[0] if not skills_df.empty else 0
    
    return stats

def get_courses_data():
    """Get all courses - SAME SQL as original"""
    query = """
    SELECT 
        course_id,
        course_name,
        description,
        category,
        duration_hours,
        difficulty_level,
        average_rating,
        total_enrollments
    FROM courses
    ORDER BY COALESCE(average_rating, 0) DESC, COALESCE(total_enrollments, 0) DESC
    """
    return execute_query(query)

def get_course_recommendations(student_id=1):
    """Get course recommendations - SAME ALGORITHM as original"""
    query = """
    SELECT 
        c.course_id,
        c.course_name,
        c.description,
        c.category,
        c.difficulty_level,
        c.average_rating,
        c.total_enrollments,
        c.duration_hours
    FROM courses c
    LEFT JOIN enrollments e ON c.course_id = e.course_id AND e.student_id = ?
    WHERE e.enrollment_id IS NULL
    ORDER BY COALESCE(c.average_rating, 0) DESC, COALESCE(c.total_enrollments, 0) DESC
    LIMIT 6
    """
    return execute_query(query, params=[student_id])

def get_enrollment_data():
    """Get enrollment analytics - SAME SQL as original"""
    query = """
    SELECT 
        c.category,
        COUNT(e.enrollment_id) as enrollment_count,
        AVG(c.average_rating) as avg_rating
    FROM courses c
    LEFT JOIN enrollments e ON c.course_id = e.course_id
    GROUP BY c.category
    ORDER BY COALESCE(enrollment_count, 0) DESC
    """
    return execute_query(query)

# Authentication functions
def hash_password(password):
    """Hash password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    """Authenticate user login"""
    query = "SELECT student_id, name, email FROM students WHERE email = ? AND password = ?"
    hashed_pw = hash_password(password)
    result = execute_query(query, params=[email, hashed_pw])
    return result.iloc[0].to_dict() if not result.empty else None

def authenticate_admin(email, password):
    """Authenticate admin login"""
    try:
        # For demo purposes, use hardcoded admin credentials
        # In production, this should be stored in a separate admin table
        if email == "admin@example.com" and password == "admin123":
            return {
                "admin_id": 1,
                "name": "System Administrator",
                "email": "admin@example.com",
                "role": "admin"
            }
        return None
    except Exception as e:
        st.error(f"Admin authentication error: {str(e)}")
        return None

def register_user(name, email, password, phone, department, year):
    """Register new user with improved error handling"""
    try:
        # Check if email already exists
        check_query = "SELECT COUNT(*) as count FROM students WHERE email = ?"
        result = execute_query(check_query, params=[email])
        
        if result.empty:
            return False, "Database connection error!", None
            
        if result['count'].iloc[0] > 0:
            return False, "Email already exists! Please use a different email.", None
        
        # Insert new user with registration_date
        insert_query = """
        INSERT INTO students (name, email, password, phone, department, year, registration_date)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """
        hashed_pw = hash_password(password)
        
        success = execute_insert(insert_query, (name, email, hashed_pw, phone, department, year))
        if success:
            # Get the new user's ID
            user_query = "SELECT student_id, name, email FROM students WHERE email = ?"
            user_result = execute_query(user_query, params=[email])
            if not user_result.empty:
                user_data = user_result.iloc[0].to_dict()
                return True, f"Registration successful! Welcome {name}!", user_data
            else:
                return True, "Registration successful! You can now login.", None
        else:
            return False, "Registration failed! Please try again.", None
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return False, f"Registration failed: {str(e)}", None

def enroll_in_course(student_id, course_id):
    """Enroll student in course"""
    try:
        # Check if already enrolled
        check_query = "SELECT COUNT(*) as count FROM enrollments WHERE student_id = ? AND course_id = ?"
        result = execute_query(check_query, params=[student_id, course_id])
        if result['count'].iloc[0] > 0:
            return False, "Already enrolled in this course!"
        
        # Add enrollment
        insert_query = """
        INSERT INTO enrollments (student_id, course_id, enrollment_date, completion_status)
        VALUES (?, ?, datetime('now'), 'Enrolled')
        """
        
        success = execute_insert(insert_query, (student_id, course_id))
        if success:
            return True, "Enrolled successfully!"
        else:
            return False, "Enrollment failed!"
    except Exception as e:
        return False, f"Enrollment failed: {str(e)}"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'is_new_user' not in st.session_state:
    st.session_state.is_new_user = False

# Sidebar navigation
def show_sidebar():
    """Show sidebar navigation"""
    if st.session_state.logged_in:
        st.sidebar.markdown("### 🤖 AI Course Recommender")
        
        st.sidebar.success(f"👋 Welcome, {st.session_state.user_data['name']}!")
        
        # Navigation menu
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📋 Navigation")
        
        # Create navigation buttons based on user type
        if st.session_state.get('user_type') == 'Admin':
            pages = [
                ("📊", "Admin Dashboard"),
                ("👥", "All Students"),
                ("📚", "All Courses"),
                ("📝", "All Enrollments"),
                ("📈", "System Analytics")
            ]
        else:
            pages = [
                ("📊", "Dashboard"),
                ("🎯", "Smart Quiz"),
                ("📚", "Browse Courses"), 
                ("📝", "My Enrollments"),
                ("🛠️", "My Skills"),
                ("🔍", "Recommendations"),
                ("💬", "Feedback")
            ]
        
        # Initialize current page
        if 'current_page' not in st.session_state:
            if st.session_state.get('user_type') == 'Admin':
                st.session_state.current_page = "Admin Dashboard"
            else:
                st.session_state.current_page = "Dashboard"
        
        # Create buttons for each page
        for icon, page_name in pages:
            if st.sidebar.button(f"{icon} {page_name}", key=f"nav_{page_name}"):
                st.session_state.current_page = page_name
                st.rerun()
        
        # Logout section
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.session_state.user_type = None
            st.rerun()
        
        return st.session_state.current_page
    else:
        # Login/Register sidebar - simplified
        st.sidebar.markdown("### 🎓 Welcome to Course Recommendation System")
        st.sidebar.markdown("---")
        
        return "Login"

# Page functions
def show_login_page(mode):
    """Show login or register page based on mode"""
    
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    
    with col2:
        # Toggle between Login and Register
        if 'show_register' not in st.session_state:
            st.session_state.show_register = False
        
        if not st.session_state.show_register:
            # LOGIN SECTION
            st.markdown('<h2 style="text-align: center; margin-top: 2rem;">🔐 Login to Your Account</h2>', unsafe_allow_html=True)
            
            # Login type selection
            login_type = st.radio("Login as:", ["Student", "Admin"], horizontal=True)
            
            with st.form("login_form"):
                if login_type == "Admin":
                    email = st.text_input("Admin Email", placeholder="admin@example.com")
                    password = st.text_input("Password", type="password", placeholder="Enter admin password")
                else:
                    email = st.text_input("Email", placeholder="student@example.com")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if email and password:
                        if login_type == "Admin":
                            user = authenticate_admin(email, password)
                        else:
                            user = authenticate_user(email, password)
                            
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_data = user
                            st.session_state.user_type = login_type
                            st.session_state.is_new_user = False  # Existing user login
                            st.success(f"Welcome back, {user['name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials!")
                    else:
                        st.error("Please fill in all fields!")
            
            # Registration option
            st.markdown("---")
            st.markdown('<p style="text-align: center; font-size: 1.1rem;">Don\'t have an account?</p>', unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("📝 Create New Account", use_container_width=True, type="secondary"):
                    st.session_state.show_register = True
                    st.rerun()
            
            if login_type == "Admin":
                st.info("💡 **Admin Login:** Use admin@example.com with password 'admin123'")
            else:
                st.info("💡 **Student Login:** Use any email from the database with password 'password123'")
            
            # Show sample students for demo
            st.subheader("Sample Students (for demo)")
            sample_students = execute_query("SELECT name, email FROM students LIMIT 5")
            if not sample_students.empty:
                st.dataframe(sample_students, use_container_width=True)
        
        else:
            # REGISTRATION SECTION
            st.markdown('<h2 style="text-align: center; margin-top: 2rem;">📝 Create New Account</h2>', unsafe_allow_html=True)
            
            with st.form("register_form"):
                name = st.text_input("Full Name", placeholder="John Doe")
                email = st.text_input("Email", placeholder="john@example.com")
                password = st.text_input("Password", type="password", placeholder="Create a secure password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                phone = st.text_input("Phone", placeholder="+91-9876543210")
                department = st.selectbox("Department", ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil", "Data Science", "AI & ML"])
                year = st.selectbox("Academic Year", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduate", "Post Graduate"])
                
                submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit:
                    if name and email and password and confirm_password:
                        if password != confirm_password:
                            st.error("Passwords do not match!")
                        elif len(password) < 6:
                            st.error("Password must be at least 6 characters long!")
                        else:
                            success, message, user_data = register_user(name, email, password, phone, department, year)
                            if success:
                                st.success(message)
                                if user_data:
                                    # Auto-login the new user
                                    st.session_state.logged_in = True
                                    st.session_state.user_data = user_data
                                    st.session_state.user_type = "Student"
                                    st.session_state.is_new_user = True  # New user registration
                                    st.session_state.show_welcome_quiz = True
                                    st.session_state.current_page = "Smart Quiz"
                                    st.success(f"Welcome {user_data['name']}! Let's find your perfect courses!")
                                    st.rerun()
                                else:
                                    st.info("Registration successful! Please login with your credentials.")
                                    st.session_state.show_register = False
                                    st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.error("Please fill in all required fields!")
            
            # Back to login option
            st.markdown("---")
            st.markdown('<p style="text-align: center; font-size: 1.1rem;">Already have an account?</p>', unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("🔐 Back to Login", use_container_width=True, type="secondary"):
                    st.session_state.show_register = False
                    st.rerun()
            
            st.info("💡 **Note:** After registration, you'll be automatically logged in and can take our Smart Quiz!")

def show_dashboard():
    """Show clean, simple dashboard"""
    
    # Check if admin
    if st.session_state.get('user_type') == 'Admin':
        show_admin_dashboard()
        return
    
    # Check if it's a new user or returning user
    is_new_user = st.session_state.get('is_new_user', False)
    welcome_text = "Welcome" if is_new_user else "Welcome back"
    journey_text = "Start your AI learning journey" if is_new_user else "Continue your AI learning journey"
    
    # Interactive Welcome Header with Animation
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; padding: 30px; margin-bottom: 20px; 
                text-align: center; color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
                animation: fadeIn 1s ease-in;">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" 
                 style="width: 60px; height: 60px; border-radius: 50%; margin-right: 20px; 
                        border: 3px solid white; animation: bounce 2s infinite;">
            <div>
                <h1 style="margin: 0; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    🚀 {welcome_text}, {st.session_state.user_data['name']}!
                </h1>
                <p style="margin: 5px 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                    Ready to {journey_text}? 🎯
                </p>
            </div>
        </div>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
            <div style="background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; 
                        backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3);">
                📚 {len(execute_query("SELECT COUNT(*) as count FROM courses").iloc[0]) if not execute_query("SELECT COUNT(*) as count FROM courses").empty else 0} Courses Available
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; 
                        backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3);">
                🎯 Personalized Recommendations
            </div>
        </div>
    </div>
    
    <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
            40% {{ transform: translateY(-10px); }}
            60% {{ transform: translateY(-5px); }}
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Get student data
    student_id = st.session_state.user_data['student_id']
    
    # Interactive Stats with Icons and Animations
    enrolled_query = "SELECT COUNT(*) as count FROM enrollments WHERE student_id = ?"
    enrolled = execute_query(enrolled_query, params=[student_id])
    enrolled_count = enrolled['count'].iloc[0] if not enrolled.empty else 0
    
    completed_query = "SELECT COUNT(*) as count FROM enrollments WHERE student_id = ? AND completion_status = 'Completed'"
    completed = execute_query(completed_query, params=[student_id])
    completed_count = completed['count'].iloc[0] if not completed.empty else 0
    
    total_query = "SELECT COUNT(*) as count FROM courses"
    total = execute_query(total_query)
    total_count = total['count'].iloc[0] if not total.empty else 0
    
    # Create stats cards using columns and metrics with custom styling
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); 
                    border-radius: 15px; padding: 25px; text-align: center; color: white;
                    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3); margin: 10px 0;">
            <div style="font-size: 3rem; margin-bottom: 15px;">📚</div>
            <h2 style="margin: 0; font-size: 2.5rem; font-weight: bold;">{enrolled_count}</h2>
            <p style="margin: 5px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Enrolled Courses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2ecc71, #27ae60); 
                    border-radius: 15px; padding: 25px; text-align: center; color: white;
                    box-shadow: 0 8px 25px rgba(46, 204, 113, 0.3); margin: 10px 0;">
            <div style="font-size: 3rem; margin-bottom: 15px;">🎓</div>
            <h2 style="margin: 0; font-size: 2.5rem; font-weight: bold;">{completed_count}</h2>
            <p style="margin: 5px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3498db, #2980b9); 
                    border-radius: 15px; padding: 25px; text-align: center; color: white;
                    box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3); margin: 10px 0;">
            <div style="font-size: 3rem; margin-bottom: 15px;">🎯</div>
            <h2 style="margin: 0; font-size: 2.5rem; font-weight: bold;">{total_count}</h2>
            <p style="margin: 5px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Available Courses</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive Quick Actions with Icons
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                border-radius: 20px; padding: 25px; margin: 30px 0; text-align: center;">
        <h2 style="color: white; margin-bottom: 20px; font-size: 1.8rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            ⚡ Quick Actions
        </h2>
        <p style="color: white; opacity: 0.9; margin-bottom: 25px;">
            Jump into your learning journey with these interactive features! 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create interactive action cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                    border-radius: 15px; padding: 20px; text-align: center; color: white;
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                    transition: transform 0.3s ease; cursor: pointer;"
                    onmouseover="this.style.transform='translateY(-5px)'"
                    onmouseout="this.style.transform='translateY(0)'">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎯</div>
            <h3 style="margin: 0; font-size: 1.1rem;">Smart Quiz</h3>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.8;">Get AI Recommendations</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎯 Take Smart Quiz", key="quiz_action", use_container_width=True, type="primary"):
            st.session_state.current_page = "Smart Quiz"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb, #f5576c); 
                    border-radius: 15px; padding: 20px; text-align: center; color: white;
                    box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
                    transition: transform 0.3s ease; cursor: pointer;"
                    onmouseover="this.style.transform='translateY(-5px)'"
                    onmouseout="this.style.transform='translateY(0)'">
            <div style="font-size: 3rem; margin-bottom: 10px;">📚</div>
            <h3 style="margin: 0; font-size: 1.1rem;">Browse Courses</h3>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.8;">Explore All Courses</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Browse Courses", key="browse_action", use_container_width=True, type="primary"):
            st.session_state.current_page = "Browse Courses"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe, #00f2fe); 
                    border-radius: 15px; padding: 20px; text-align: center; color: white;
                    box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
                    transition: transform 0.3s ease; cursor: pointer;"
                    onmouseover="this.style.transform='translateY(-5px)'"
                    onmouseout="this.style.transform='translateY(0)'">
            <div style="font-size: 3rem; margin-bottom: 10px;">🔍</div>
            <h3 style="margin: 0; font-size: 1.1rem;">Recommendations</h3>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.8;">Personalized Picks</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Recommendations", key="rec_action", use_container_width=True, type="primary"):
            st.session_state.current_page = "Recommendations"
            st.rerun()
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b, #38f9d7); 
                    border-radius: 15px; padding: 20px; text-align: center; color: white;
                    box-shadow: 0 8px 25px rgba(67, 233, 123, 0.3);
                    transition: transform 0.3s ease; cursor: pointer;"
                    onmouseover="this.style.transform='translateY(-5px)'"
                    onmouseout="this.style.transform='translateY(0)'">
            <div style="font-size: 3rem; margin-bottom: 10px;">📝</div>
            <h3 style="margin: 0; font-size: 1.1rem;">My Progress</h3>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.8;">Track Learning</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 My Progress", key="progress_action", use_container_width=True, type="primary"):
            st.session_state.current_page = "My Enrollments"
            st.rerun()
    
    # Recent Activity - Only if user has enrollments
    if enrolled_count > 0:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 20px; padding: 25px; margin: 30px 0;">
            <h2 style="color: white; margin-bottom: 20px; font-size: 1.8rem; text-align: center;">
                📝 Recent Activity
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        recent_query = """
        SELECT c.course_name, e.completion_status, e.enrollment_date
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        WHERE e.student_id = ?
        ORDER BY e.enrollment_date DESC
        LIMIT 3
        """
        recent = execute_query(recent_query, params=[student_id])
        
        if not recent.empty:
            for idx, (_, row) in enumerate(recent.iterrows()):
                status_color = "#2ecc71" if row['completion_status'] == 'Completed' else "#f39c12"
                status_icon = "✅" if row['completion_status'] == 'Completed' else "📚"
                status_text = "Completed" if row['completion_status'] == 'Completed' else "In Progress"
                
                st.markdown(f"""
                <div style="background: white; border-radius: 15px; padding: 25px; margin: 15px 0; 
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid {status_color};">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <h3 style="margin: 0; color: #2c3e50; font-size: 1.3rem;">{row['course_name']}</h3>
                            <p style="margin: 5px 0 0 0; color: #7f8c8d; font-size: 0.9rem;">
                                Enrolled: {row['enrollment_date'][:10]}
                            </p>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 2rem; margin-bottom: 5px;">{status_icon}</div>
                            <span style="background: {status_color}; color: white; padding: 5px 15px; 
                                       border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                                {status_text}
                            </span>
                        </div>
                    </div>
                    
                    {f'''
                    <!-- Progress Bar - Only for Completed Courses -->
                    <div style="margin-top: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 0.9rem; color: #666; font-weight: 600;">Course Completed</span>
                            <span style="font-size: 0.9rem; color: {status_color}; font-weight: bold;">100%</span>
                        </div>
                        <div style="background: #f0f0f0; border-radius: 10px; height: 8px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, {status_color}, {status_color}aa); 
                                       height: 100%; width: 100%; border-radius: 10px;
                                       transition: width 0.5s ease;"></div>
                        </div>
                        <div style="text-align: center; margin-top: 10px;">
                            <span style="background: #e8f5e8; color: #2ecc71; padding: 5px 15px; 
                                       border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                                🎓 Certificate Earned
                            </span>
                        </div>
                    </div>
                    ''' if row['completion_status'] == 'Completed' else ''}
                </div>
                """, unsafe_allow_html=True)
    
    # If no enrollments, show recommendation
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                    border-radius: 20px; padding: 40px; margin: 30px 0; text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 20px;">🚀</div>
            <h2 style="color: white; margin-bottom: 15px; font-size: 2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                Ready to Start Your Learning Journey?
            </h2>
            <p style="color: white; font-size: 1.2rem; margin-bottom: 25px; opacity: 0.9;">
                Take our Smart Quiz to get personalized AI course recommendations! 🎯
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Smart Quiz", use_container_width=True, type="primary"):
                st.session_state.current_page = "Smart Quiz"
                st.rerun()

def show_courses_page():
    """Show courses page with modern card-based layout"""
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    st.markdown('<h2 style=";">📚 Explore All Courses</h2>', unsafe_allow_html=True)
    
    # Filter Section
    st.markdown('<div class="card-header" style="margin-top: 20px;">🔍 Filter Courses</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    courses_df = get_courses_data()
    
    if not courses_df.empty:
        with col1:
            categories = ['All'] + sorted(courses_df['category'].unique().tolist())
            selected_category = st.selectbox("📚 Category", categories)
        
        with col2:
            difficulties = ['All'] + sorted(courses_df['difficulty_level'].unique().tolist())
            selected_difficulty = st.selectbox("📊 Difficulty", difficulties)
        
        with col3:
            min_rating = st.slider("⭐ Minimum Rating", 0.0, 5.0, 0.0, 0.1)
        
        # Filter courses
        filtered_courses = courses_df.copy()
        
        if selected_category != 'All':
            filtered_courses = filtered_courses[filtered_courses['category'] == selected_category]
        
        if selected_difficulty != 'All':
            filtered_courses = filtered_courses[filtered_courses['difficulty_level'] == selected_difficulty]
        
        # Handle None values for rating filter
        filtered_courses = filtered_courses[
            filtered_courses['average_rating'].fillna(0.0) >= min_rating
        ]
        
        # Display courses in cards - SIDE BY SIDE
        st.markdown(f'<div class="card-header">📚 Available Courses ({len(filtered_courses)} found)</div>', unsafe_allow_html=True)
        
        # Display courses in 2 columns
        for i in range(0, len(filtered_courses), 2):
            cols = st.columns(2)
            
            for col_idx, (_, course) in enumerate(filtered_courses.iloc[i:i+2].iterrows()):
                with cols[col_idx]:
                    rating = course['average_rating'] if course['average_rating'] is not None else 0.0
                    enrollments = course['total_enrollments'] if course['total_enrollments'] is not None else 0
                    
                    st.markdown(f'''
                    <div class="course-card">
                        <h3>📚 {course['course_name']}</h3>
                        <p><strong>📚 {course['category']} • ⏱️ {course['duration_hours']}h • 📊 {course['difficulty_level']}</strong></p>
                        <p>{course['description'][:100]}...</p>
                        <div style="text-align: center; margin-top: 15px;">
                            <span style="font-size: 1.4rem; color: #ff6b35; font-weight: bold;">⭐ {rating:.1f}/5.0</span>
                            <span style="margin-left: 20px; color: #666;">👥 {enrollments} students</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Add enrollment button
                    if st.button(f"Enroll Now", key=f"enroll_{course['course_id']}", use_container_width=True):
                        success, message = enroll_in_course(st.session_state.user_data['student_id'], course['course_id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
    else:
        st.markdown('<div class="card"><p>No courses available at the moment.</p></div>', unsafe_allow_html=True)

def show_smart_quiz():
    """Interactive step-by-step questionnaire for personalized course recommendations"""
    
    # Initialize quiz state
    if 'quiz_step' not in st.session_state:
        st.session_state.quiz_step = 0
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    
    # Check if this is a new registration flow
    is_new_user = st.session_state.get('show_welcome_quiz', False)
    
    if is_new_user:
        st.markdown('<h1>🎉 Welcome! Let\'s Find Your Perfect AI Courses</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div class="quiz-container">
            <h2 style="text-align: center; margin-bottom: 20px;">🤖 AI Learning Path Discovery</h2>
            <p style="font-size: 1.2rem; text-align: center; margin-bottom: 0;">
                Discover your personalized AI learning journey! This will only take 2 minutes! 🚀
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<h1>🤖 AI Course Finder</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div class="quiz-container">
            <h2 style="text-align: center; margin-bottom: 20px;">🎓 Discover Your AI Learning Path</h2>
            <p style="font-size: 1.2rem; text-align: center; margin-bottom: 0;">
                Answer a few questions and get personalized AI course recommendations! 🚀
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Reset quiz button (only if not new user)
    if not is_new_user:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.session_state.quiz_completed and st.button("🔄 Start Over", use_container_width=True):
                st.session_state.quiz_step = 0
                st.session_state.quiz_answers = {}
                st.session_state.quiz_completed = False
                st.rerun()
    
    if not st.session_state.quiz_completed:
        show_interactive_quiz_step()
    else:
        # Clear the welcome flag after completing quiz
        if 'show_welcome_quiz' in st.session_state:
            del st.session_state['show_welcome_quiz']
        show_quiz_recommendations()

def show_interactive_quiz_step():
    """Show one question at a time with interactive UI"""
    questions = list(QUESTIONNAIRE.items())
    current_step = st.session_state.quiz_step
    total_steps = len(questions)
    
    # Progress bar
    progress = (current_step + 1) / total_steps
    st.markdown(f"""
    <div class="quiz-container">
        <h3 style="text-align: center; margin-bottom: 20px;">Question {current_step + 1} of {total_steps}</h3>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress)
    
    if current_step < total_steps:
        key, data = questions[current_step]
        
        # Display current question
        st.markdown(f"""
        <div class="quiz-step">
            <h2 style="text-align: center; margin-bottom: 25px; color: white;">{data['question']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Create interactive buttons for options
        options = list(data['options'].keys())
        
        # Display options as clickable cards
        cols = st.columns(min(len(options), 2))  # Max 2 columns
        
        for i, option in enumerate(options):
            col_idx = i % 2
            with cols[col_idx]:
                # Create a unique key for each option button
                button_key = f"option_{current_step}_{i}"
                
                if st.button(
                    option, 
                    key=button_key,
                    use_container_width=True,
                    help=f"Click to select: {option}"
                ):
                    # Store the answer
                    st.session_state.quiz_answers[key] = {
                        'answer': option,
                        'value': data['options'][option]
                    }
                    
                    # Move to next question
                    if current_step < total_steps - 1:
                        st.session_state.quiz_step += 1
                        st.rerun()
                    else:
                        # Quiz completed
                        st.session_state.quiz_completed = True
                        st.rerun()
        
        # Navigation buttons
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if current_step > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.quiz_step -= 1
                    st.rerun()
        
        with col3:
            # Show current answer if exists
            if key in st.session_state.quiz_answers:
                current_answer = st.session_state.quiz_answers[key]['answer']
                st.success(f"✅ Selected: {current_answer}")
                
                if st.button("Next ➡️", use_container_width=True):
                    if current_step < total_steps - 1:
                        st.session_state.quiz_step += 1
                        st.rerun()
                    else:
                        st.session_state.quiz_completed = True
                        st.rerun()
    
    # Show summary of answers so far
    if st.session_state.quiz_answers:
        with st.expander("📋 Your Answers So Far"):
            for q_key, answer_data in st.session_state.quiz_answers.items():
                question_text = QUESTIONNAIRE[q_key]['question']
                st.write(f"**{question_text}**")
                st.write(f"✅ {answer_data['answer']}")
                st.write("---")

def show_quiz_recommendations():
    """Display personalized recommendations based on quiz answers"""
    st.markdown('<h2>🎉 Your Personalized Course Recommendations</h2>', unsafe_allow_html=True)
    
    answers = st.session_state.quiz_answers
    
    # Analyze answers to determine recommended categories
    recommended_categories = set()
    
    # Add categories based on career goal
    if 'career_goal' in answers:
        career_categories = answers['career_goal']['value']
        if isinstance(career_categories, list):
            recommended_categories.update(career_categories)
    
    # Add categories based on interest area
    if 'interest_area' in answers:
        interest_categories = answers['interest_area']['value']
        if isinstance(interest_categories, list):
            recommended_categories.update(interest_categories)
    
    # Get experience level
    experience_level = answers.get('experience_level', {}).get('value', 'Beginner')
    time_commitment = answers.get('time_commitment', {}).get('answer', '4-7 hours')
    learning_style = answers.get('learning_style', {}).get('answer', 'Video Lectures with Quizzes')
    
    # Display profile summary
    st.markdown(f"""
    <div class="card">
        <h3 style="text-align: center; color: #667eea; margin-bottom: 20px;">📋 Your Learning Profile</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div style="background: #f7fafc; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                <strong style="color: #667eea;">🎯 Career Goal:</strong><br>
                <span style="color: #4a5568;">{answers.get('career_goal', {}).get('answer', 'N/A')}</span>
            </div>
            <div style="background: #f7fafc; padding: 15px; border-radius: 10px; border-left: 4px solid #f093fb;">
                <strong style="color: #f093fb;">📊 Experience:</strong><br>
                <span style="color: #4a5568;">{experience_level}</span>
            </div>
            <div style="background: #f7fafc; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                <strong style="color: #667eea;">⏰ Time Commitment:</strong><br>
                <span style="color: #4a5568;">{time_commitment}</span>
            </div>
            <div style="background: #f7fafc; padding: 15px; border-radius: 10px; border-left: 4px solid #f093fb;">
                <strong style="color: #f093fb;">🎓 Learning Style:</strong><br>
                <span style="color: #4a5568;">{learning_style}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display recommended courses with platform links
    st.markdown('<h3 style="margin-top: 30px;">🚀 Recommended Courses for You</h3>', unsafe_allow_html=True)
    
    if not recommended_categories:
        recommended_categories = ['Python Programming', 'Web Development']
    
    for idx, category in enumerate(sorted(recommended_categories), 1):
        if category in COURSE_PLATFORMS:
            st.markdown(f"""
            <div class="course-card">
                <h3>#{idx} {category}</h3>
                <p><strong>🎯 Why this course?</strong> Based on your {answers.get('career_goal', {}).get('answer', 'career goals')} 
                and {answers.get('interest_area', {}).get('answer', 'interests')}, this is perfect for you!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display platform links
            st.markdown('<div style="margin-left: 20px; margin-bottom: 20px;">', unsafe_allow_html=True)
            st.markdown("**📚 Available on these platforms:**")
            
            for platform_info in COURSE_PLATFORMS[category]:
                badge_html = f"""
                <div style="margin: 10px 0; padding: 15px; background: white; border-radius: 10px; 
                     border: 2px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="platform-badge {platform_info['badge']}">{platform_info['platform']}</span>
                        <strong style="color: #2d3748; margin-left: 10px;">{platform_info['name']}</strong>
                    </div>
                    <a href="{platform_info['url']}" target="_blank" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 8px 20px; border-radius: 8px; 
                              text-decoration: none; font-weight: 600;">
                        View Course →
                    </a>
                </div>
                """
                st.markdown(badge_html, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Match with database courses
    st.markdown('<h3 style="margin-top: 30px;">💎 Featured Courses from Our Database</h3>', unsafe_allow_html=True)
    
    # Get matching courses from database
    category_list = "','".join(recommended_categories)
    query = f"""
    SELECT 
        course_id,
        course_name,
        description,
        category,
        difficulty_level,
        duration_hours,
        average_rating,
        total_enrollments
    FROM courses
    WHERE category IN ('{category_list}')
    AND difficulty_level = '{experience_level}'
    ORDER BY COALESCE(average_rating, 0) DESC, COALESCE(total_enrollments, 0) DESC
    LIMIT 5
    """
    
    matching_courses = execute_query(query)
    
    if not matching_courses.empty:
        for _, course in matching_courses.iterrows():
            rating = course['average_rating'] if course['average_rating'] is not None else 0.0
            enrollments = course['total_enrollments'] if course['total_enrollments'] is not None else 0
            
            st.markdown(f'''
            <div class="course-card">
                <h4>📚 {course['course_name']}</h4>
                <p><strong>📚 {course['category']} • ⏱️ {course['duration_hours']}h • 📊 {course['difficulty_level']}</strong></p>
                <p>{course['description'][:150]}...</p>
                <div style="text-align: center; margin-top: 15px;">
                    <span style="font-size: 1.3rem; color: #f5576c; font-weight: bold;">⭐ {rating:.1f}/5.0</span>
                    <span style="margin-left: 20px; color: #667eea; font-weight: 600;">👥 {enrollments} students enrolled</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button(f"Enroll in {course['course_name'][:25]}...", key=f"quiz_enroll_{course['course_id']}", type="secondary"):
                    success, message = enroll_in_course(st.session_state.user_data['student_id'], course['course_id'])
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.info("No matching courses found in our database. Check out the platform recommendations above!")

def show_recommendations_page():
    """Show recommendations page - SAME ALGORITHM as original"""
    st.markdown('<h2 style="color: #1f77b4; margin-bottom: 1rem;">🔍 Course Recommendations</h2>', unsafe_allow_html=True)
    
    st.info("💡 Recommendations based on your skills and preferences")
    
    recommendations = get_course_recommendations(st.session_state.user_data['student_id'])
    
    if not recommendations.empty:
        st.subheader(f"🎯 {len(recommendations)} Recommended Courses")
        
        for _, course in recommendations.iterrows():
            with st.container():
                st.markdown(f"### 📚 {course['course_name']}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**Category:** {course['category']}")
                with col2:
                    st.write(f"**Duration:** {course['duration_hours']}h")
                with col3:
                    st.write(f"**Level:** {course['difficulty_level']}")
                with col4:
                    rating = course['average_rating'] if course['average_rating'] is not None else 0.0
                    st.write(f"**Rating:** ⭐ {rating:.1f}")
                
                st.write(f"**Description:** {course['description']}")
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Enroll Now", key=f"rec_enroll_{course['course_id']}"):
                        success, message = enroll_in_course(st.session_state.user_data['student_id'], course['course_id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                
                st.divider()
    else:
        st.info("No recommendations available at the moment.")

def show_my_enrollments():
    """Show user's enrollments with Excel export"""
    st.markdown('<h2 style="color: #1f77b4; margin-bottom: 1rem;">📝 My Enrollments</h2>', unsafe_allow_html=True)
    
    # Get user's enrollments
    query = """
    SELECT 
        e.enrollment_id,
        c.course_name,
        c.category,
        c.difficulty_level,
        c.duration_hours,
        e.enrollment_date,
        e.completion_status
    FROM enrollments e
    JOIN courses c ON e.course_id = c.course_id
    WHERE e.student_id = ?
    ORDER BY e.enrollment_date DESC
    """
    
    enrollments_df = execute_query(query, params=[st.session_state.user_data['student_id']])
    
    if not enrollments_df.empty:
        st.subheader(f"📚 Your Enrolled Courses ({len(enrollments_df)} courses)")
        
        # Display enrollments
        for _, enrollment in enrollments_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{enrollment['course_name']}**")
                    st.write(f"📚 {enrollment['category']} • ⏱️ {enrollment['duration_hours']}h • 📊 {enrollment['difficulty_level']}")
                with col2:
                    st.write(f"📅 {enrollment['enrollment_date'][:10]}")
                with col3:
                    if enrollment['completion_status'] == 'Enrolled':
                        st.success(f"✅ {enrollment['completion_status']}")
                    else:
                        st.warning(f"⚠️ {enrollment['completion_status']}")
                st.divider()
        
        # Excel Export - Only for Admin users
        if st.session_state.get('user_type') == 'Admin':
            st.subheader("📊 Export Data")
            
            # Convert to Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                enrollments_df.to_excel(writer, sheet_name='My Enrollments', index=False)
                
                # Add summary sheet
                summary_data = {
                    'Metric': ['Total Enrollments', 'Enrolled', 'Completed Enrollments'],
                    'Count': [
                        len(enrollments_df),
                        len(enrollments_df[enrollments_df['completion_status'] == 'Enrolled']),
                        len(enrollments_df[enrollments_df['completion_status'] == 'Completed'])
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            output.seek(0)
            
            st.download_button(
                label="📥 Download Excel Report",
                data=output.getvalue(),
                file_name=f"my_enrollments_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            # Show info for non-admin users
            st.info("💡 **Note:** Export functionality is available only for administrators.")
        
    else:
        st.info("You haven't enrolled in any courses yet!")
        st.markdown("### 🎯 Get Started")
        st.write("1. Go to **Browse Courses** to explore available courses")
        st.write("2. Check **Recommendations** for personalized suggestions")
        st.write("3. Enroll in courses that interest you!")

# Main application
def main():
    """Main application function"""
    
    # Show sidebar and get selected page/mode
    selected_page = show_sidebar()
    
    # Route to appropriate page
    if not st.session_state.logged_in:
        show_login_page(selected_page)  # selected_page will be "Login" or "Register"
    else:
        # Admin pages
        if selected_page == "Admin Dashboard":
            show_admin_dashboard()
        elif selected_page == "All Students":
            show_all_students()
        elif selected_page == "All Courses":
            show_all_courses()
        elif selected_page == "All Enrollments":
            show_all_enrollments()
        elif selected_page == "System Analytics":
            show_system_analytics()
        # Student pages
        elif selected_page == "Dashboard":
            show_dashboard()
        elif selected_page == "Smart Quiz":
            show_smart_quiz()
        elif selected_page == "Browse Courses":
            show_courses_page()
        elif selected_page == "Recommendations":
            show_recommendations_page()
        elif selected_page == "My Enrollments":
            show_my_enrollments()
        elif selected_page == "My Skills":
            st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
            st.markdown('<h1 class="main-header">🛠️ My Skills</h1>', unsafe_allow_html=True)
            st.info("🚧 Skills management page - Coming soon!")
            st.markdown("""
            **Planned Features:**
            - View your current skills
            - Add new skills  
            - Update skill proficiency levels
            - Get skill-based course recommendations
            """)
        elif selected_page == "Feedback":
            st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
            st.markdown('<h1 class="main-header">💬 Feedback</h1>', unsafe_allow_html=True)
            st.info("🚧 Feedback page - Coming soon!")

# Admin Dashboard Functions
def show_admin_dashboard():
    """Show admin dashboard with system statistics"""
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #1f77b4; margin-bottom: 1rem; text-align: center;">📊 Admin Dashboard</h2>', unsafe_allow_html=True)
    
    # System Statistics
    st.markdown('<div class="card-header">📈 System Overview</div>', unsafe_allow_html=True)
    
    # Get system statistics
    stats_query = """
    SELECT 
        (SELECT COUNT(*) FROM students) as total_students,
        (SELECT COUNT(*) FROM courses) as total_courses,
        (SELECT COUNT(*) FROM enrollments) as total_enrollments,
        (SELECT COUNT(*) FROM skills) as total_skills
    """
    stats = execute_query(stats_query)
    
    if not stats.empty:
        stat = stats.iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number">{stat['total_students']}</div>
                <div class="stat-label">👥 Total Students</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number">{stat['total_courses']}</div>
                <div class="stat-label">📚 Total Courses</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number">{stat['total_enrollments']}</div>
                <div class="stat-label">📝 Total Enrollments</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number">{stat['total_skills']}</div>
                <div class="stat-label">🛠️ Available Skills</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Additional Admin Dashboard Content
    st.markdown("---")
    
    # Quick Actions Section
    st.markdown('<div class="card-header">⚡ Quick Actions</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 View Analytics", use_container_width=True, type="primary"):
            st.session_state.current_page = "System Analytics"
            st.rerun()
    
    with col2:
        if st.button("👥 Manage Students", use_container_width=True, type="primary"):
            st.session_state.current_page = "All Students"
            st.rerun()
    
    with col3:
        if st.button("📚 Manage Courses", use_container_width=True, type="primary"):
            st.session_state.current_page = "All Courses"
            st.rerun()
    
    with col4:
        if st.button("📝 View Enrollments", use_container_width=True, type="primary"):
            st.session_state.current_page = "All Enrollments"
            st.rerun()
    
    # Recent Activity Section
    st.markdown('<div class="card-header">📈 Recent System Activity</div>', unsafe_allow_html=True)
    
    # Get recent enrollments
    recent_enrollments_query = """
    SELECT 
        s.name as student_name,
        c.course_name,
        e.enrollment_date,
        e.completion_status
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_id = c.course_id
    ORDER BY e.enrollment_date DESC
    LIMIT 5
    """
    recent_enrollments = execute_query(recent_enrollments_query)
    
    if not recent_enrollments.empty:
        for _, row in recent_enrollments.iterrows():
            status_color = "#2ecc71" if row['completion_status'] == 'Completed' else "#f39c12"
            status_icon = "✅" if row['completion_status'] == 'Completed' else "📚"
            
            st.markdown(f"""
            <div style="background: white; border-radius: 10px; padding: 15px; margin: 10px 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid {status_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #2c3e50;">{row['student_name']}</strong> enrolled in 
                        <strong style="color: #3498db;">{row['course_name']}</strong>
                        <br><small style="color: #7f8c8d;">{row['enrollment_date'][:10]}</small>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem;">{status_icon}</div>
                        <span style="background: {status_color}; color: white; padding: 3px 10px; 
                                   border-radius: 12px; font-size: 0.7rem; font-weight: bold;">
                            {row['completion_status']}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent enrollments found.")
    
    # System Health Section
    st.markdown('<div class="card-header">💚 System Health</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Database health
        try:
            test_query = execute_query("SELECT COUNT(*) as count FROM students")
            st.success("✅ Database: Connected")
        except:
            st.error("❌ Database: Error")
    
    with col2:
        # System status
        st.success("✅ System: Online")
    
    with col3:
        # Performance
        st.success("✅ Performance: Good")

def show_all_students():
    """Show all students for admin management"""
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #1f77b4; margin-bottom: 1rem; text-align: center;">👥 All Students</h2>', unsafe_allow_html=True)
    
    # Get all students
    students_query = """
    SELECT 
        student_id,
        name,
        email,
        phone,
        department,
        year,
        registration_date
    FROM students 
    ORDER BY registration_date DESC
    """
    students_df = execute_query(students_query)
    
    if not students_df.empty:
        st.markdown('<div class="card-header">📋 Student Records</div>', unsafe_allow_html=True)
        st.dataframe(students_df, width='stretch')
        
        # Export option
        if st.button("📥 Export Students to Excel"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                students_df.to_excel(writer, sheet_name='All Students', index=False)
            output.seek(0)
            st.download_button(
                label="Download Excel File",
                data=output.getvalue(),
                file_name=f"all_students_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("No students found!")

def show_all_courses():
    """Show all courses for admin management"""
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #1f77b4; margin-bottom: 1rem; text-align: center;">📚 All Courses</h2>', unsafe_allow_html=True)
    
    # Get all courses with statistics
    courses_query = """
    SELECT 
        c.course_id,
        c.course_name,
        c.category,
        c.difficulty_level,
        c.duration_hours,
        c.description,
        COALESCE(AVG(f.rating), 0) as average_rating,
        COUNT(e.enrollment_id) as total_enrollments
    FROM courses c
    LEFT JOIN enrollments e ON c.course_id = e.course_id
    LEFT JOIN feedback f ON c.course_id = f.course_id
    GROUP BY c.course_id, c.course_name, c.category, c.difficulty_level, c.duration_hours, c.description
    ORDER BY c.course_name
    """
    courses_df = execute_query(courses_query)
    
    if not courses_df.empty:
        st.markdown('<div class="card-header">📋 Course Management</div>', unsafe_allow_html=True)
        st.dataframe(courses_df, width='stretch')
        
        # Export option
        if st.button("📥 Export Courses to Excel"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                courses_df.to_excel(writer, sheet_name='All Courses', index=False)
            output.seek(0)
            st.download_button(
                label="Download Excel File",
                data=output.getvalue(),
                file_name=f"all_courses_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("No courses found!")

def show_all_enrollments():
    """Show all enrollments for admin management"""
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #1f77b4; margin-bottom: 1rem; text-align: center;">📝 All Enrollments</h2>', unsafe_allow_html=True)
    
    # Get all enrollments with student and course details
    enrollments_query = """
    SELECT 
        e.enrollment_id,
        s.name as student_name,
        s.email as student_email,
        c.course_name,
        c.category,
        e.enrollment_date,
        e.completion_status
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_id = c.course_id
    ORDER BY e.enrollment_date DESC
    """
    enrollments_df = execute_query(enrollments_query)
    
    if not enrollments_df.empty:
        st.markdown('<div class="card-header">📋 Enrollment Records</div>', unsafe_allow_html=True)
        st.dataframe(enrollments_df, width='stretch')
        
        # Export option
        if st.button("📥 Export Enrollments to Excel"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                enrollments_df.to_excel(writer, sheet_name='All Enrollments', index=False)
            output.seek(0)
            st.download_button(
                label="Download Excel File",
                data=output.getvalue(),
                file_name=f"all_enrollments_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("No enrollments found!")

def show_system_analytics():
    """Show comprehensive system analytics for admin"""
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #1f77b4; margin-bottom: 1rem; text-align: center;">📈 System Analytics</h2>', unsafe_allow_html=True)
    
    # Enrollment trends by category
    st.markdown('<div class="card-header">📊 Enrollment Analytics</div>', unsafe_allow_html=True)
    
    analytics_query = """
    SELECT 
        c.category,
        COUNT(e.enrollment_id) as enrollment_count,
        AVG(COALESCE(f.rating, 0)) as avg_rating
    FROM courses c
    LEFT JOIN enrollments e ON c.course_id = e.course_id
    LEFT JOIN feedback f ON c.course_id = f.course_id
    GROUP BY c.category
    ORDER BY enrollment_count DESC
    """
    analytics_df = execute_query(analytics_query)
    
    if not analytics_df.empty:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Bar chart for enrollments by category
            fig_bar = px.bar(
                analytics_df, 
                x='category', 
                y='enrollment_count',
                title="Enrollments by Category",
                color='enrollment_count',
                color_continuous_scale='viridis',
                width=600,
                height=400
            )
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_bar)
        
        with col2:
            # Pie chart for category distribution
            fig_pie = px.pie(
                analytics_df, 
                values='enrollment_count', 
                names='category',
                title="Category Distribution",
                width=400,
                height=400
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_pie)
        
        # Display analytics table
        st.markdown('<div class="card-header">📋 Analytics Summary</div>', unsafe_allow_html=True)
        st.dataframe(analytics_df, width='stretch')
    else:
        st.info("No analytics data available!")

if __name__ == "__main__":
    main()
