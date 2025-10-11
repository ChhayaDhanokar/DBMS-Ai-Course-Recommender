# 🤖 AI Course Recommendation System

A comprehensive AI-powered course recommendation system built with Streamlit and SQLite database, featuring intelligent course suggestions based on user preferences and learning goals.

## 🌟 Features

### 🎯 **Smart Course Recommendations**
- AI-powered questionnaire to understand learning preferences
- Personalized course suggestions based on career goals
- Interactive quiz system with step-by-step guidance
- Real-time course filtering and search capabilities

### 👥 **User Management**
- Student registration and authentication system
- Admin panel for system management
- Role-based access control (Student/Admin)
- Secure password hashing and session management

### 📊 **Analytics & Reporting**
- Comprehensive admin dashboard with system statistics
- Course enrollment analytics and trends
- Export functionality for administrators (Excel reports)
- Real-time system health monitoring

### 🎨 **Modern UI/UX**
- Beautiful, responsive Streamlit interface
- Interactive progress bars for completed courses
- Gradient backgrounds and smooth animations
- Mobile-friendly design with glassmorphism effects

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Streamlit
- SQLite3

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PremBorde/DBMS--Ai-Course-Recommender.git
   cd DBMS--Ai-Course-Recommender
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas plotly sqlite3
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - Use admin credentials: `admin@example.com` / `admin123`
   - Or register as a new student

## 📁 Project Structure

```
DBMS/
├── streamlit_app.py          # Main Streamlit application
├── backend/
│   ├── app_sqlite.py         # Flask backend (alternative)
│   └── course_recommendation.db  # SQLite database
├── schema.sql               # Database schema
├── sample_data.sql          # Sample course data
├── dbms_queries.sql         # Database queries
├── advanced_concepts.sql    # Advanced SQL concepts
└── add_more_courses.py      # Course data management
```

## 🎯 Key Components

### **1. Smart Quiz System**
- Interactive questionnaire with 5 key questions
- Career goal mapping to course categories
- Experience level assessment
- Learning style preferences
- Time commitment evaluation

### **2. Course Database**
- 28+ AI and technology courses
- Multiple difficulty levels (Beginner, Intermediate, Advanced)
- Course ratings and enrollment statistics
- Category-based organization

### **3. Admin Dashboard**
- System overview with key metrics
- Student management capabilities
- Course management tools
- Enrollment analytics and reporting
- Export functionality for data analysis

## 🔧 Technical Features

- **Database**: SQLite with relational schema
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with pandas for data processing
- **Authentication**: Session-based with password hashing
- **Export**: Excel reports with multiple sheets
- **Responsive**: Mobile-friendly interface design

## 📊 Database Schema

- **Students**: User profiles and authentication
- **Courses**: Course catalog with metadata
- **Enrollments**: Student-course relationships
- **Skills**: Skill tracking and management
- **Feedback**: Course ratings and reviews

## 🎨 UI Features

- **Gradient backgrounds** with modern color schemes
- **Interactive animations** and hover effects
- **Progress bars** for course completion tracking
- **Card-based layouts** for better content organization
- **Responsive design** for all screen sizes

## 🔐 Security Features

- Password hashing with SHA-256
- Session management and authentication
- Role-based access control
- Input validation and sanitization
- Admin-only export functionality

## 📈 Future Enhancements

- Machine learning-based recommendations
- Advanced analytics and reporting
- Course progress tracking
- Certificate generation
- Social learning features
- Mobile app development

## 👨‍💻 Author

**Prem Borde**
- GitHub: [@PremBorde](https://github.com/PremBorde)
- Project: AI Course Recommendation System

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, email support@example.com or create an issue in the GitHub repository.

---

⭐ **Star this repository if you found it helpful!**
