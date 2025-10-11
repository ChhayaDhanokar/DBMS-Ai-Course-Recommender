import sqlite3

DB_PATH = 'backend/course_recommendation.db'

# Additional courses to add
new_courses = [
    ('Complete Python Bootcamp', 'Learn Python from scratch to advanced level...', 'Programming', 40, 'Beginner', 5.0, 2),
    ('SQL Mastery', 'Master SQL queries, joins, and database design...', 'Database', 35, 'Beginner', 4.8, 15),
    ('Cloud Computing Fundamentals', 'Introduction to AWS, Azure, and cloud services...', 'Cloud Computing', 45, 'Intermediate', 4.6, 18),
    ('Cybersecurity Essentials', 'Learn network security, cryptography, and ethical hacking...', 'Cybersecurity', 55, 'Intermediate', 4.7, 12),
    ('Mobile App Development', 'Build iOS and Android apps using React Native...', 'Mobile Development', 70, 'Intermediate', 4.5, 20),
    ('Blockchain Technology', 'Understand blockchain, cryptocurrencies, and smart contracts...', 'Blockchain', 50, 'Advanced', 4.4, 8),
    ('IoT with Arduino', 'Create Internet of Things projects with Arduino and sensors...', 'IoT', 38, 'Beginner', 4.3, 14),
    ('Digital Marketing Analytics', 'Data-driven marketing strategies and analytics tools...', 'Business Analytics', 42, 'Beginner', 4.5, 25),
    ('Agile Project Management', 'Scrum, Kanban, and agile methodologies for project management...', 'Project Management', 30, 'Beginner', 4.6, 30),
    ('Advanced Python for Data Science', 'Advanced Python techniques for data manipulation and analysis...', 'Data Science', 65, 'Advanced', 4.8, 10),
    ('Kubernetes for Developers', 'Container orchestration with Kubernetes and microservices...', 'DevOps', 48, 'Advanced', 4.7, 7),
    ('Natural Language Processing', 'NLP techniques, sentiment analysis, and chatbot development...', 'AI/ML', 75, 'Advanced', 4.9, 6),
    ('Computer Vision with OpenCV', 'Image processing, object detection, and computer vision projects...', 'AI/ML', 68, 'Advanced', 4.8, 9),
    ('GraphQL API Development', 'Build modern APIs with GraphQL, Apollo, and React...', 'Web Development', 42, 'Intermediate', 4.4, 16),
    ('Serverless Architecture', 'AWS Lambda, API Gateway, and serverless application design...', 'Cloud Computing', 40, 'Intermediate', 4.5, 11),
    ('Ethical Hacking Basics', 'Learn penetration testing and security assessment techniques...', 'Cybersecurity', 60, 'Intermediate', 4.6, 13),
    ('Game Development with Unity', 'Create 2D and 3D games using Unity game engine...', 'Game Development', 80, 'Beginner', 4.7, 22),
    ('Flutter Mobile Development', 'Cross-platform app development with Flutter and Dart...', 'Mobile Development', 58, 'Intermediate', 4.5, 17),
    ('Quantum Computing Basics', 'Introduction to quantum computing concepts and applications...', 'Emerging Tech', 45, 'Advanced', 4.3, 5),
    ('AR/VR Development', 'Build Augmented and Virtual Reality applications...', 'Emerging Tech', 62, 'Advanced', 4.4, 8),
]

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert new courses
    cursor.executemany(
        """INSERT INTO courses (course_name, description, category, duration_hours, 
           difficulty_level, average_rating, total_enrollments) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        new_courses
    )
    
    conn.commit()
    print(f"✅ Successfully added {len(new_courses)} more courses!")
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM courses")
    total = cursor.fetchone()[0]
    print(f"📚 Total courses in database: {total}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")


