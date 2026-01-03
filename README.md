# 🎓 EDMS - Education Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Language](https://img.shields.io/badge/Language-Turkmen-red.svg)](README.md)

Modern, secure, and feature-rich school management system built with Flask. Fully localized in Turkmen language with real-time lesson tracking, voice notifications, and mobile-responsive design.

## ✨ Features

### 🎯 Role-Based Access Control
- **Director**: Full system control, user management, schedule creation
- **Teacher**: Attendance tracking, grade management, lesson planning
- **Student**: View schedules, grades, homework, notifications
- **Parent**: Monitor children's progress and attendance

### 📚 Core Functionality
- ✅ **User Management** - Create, edit, delete users with role-based permissions
- ✅ **Class & Subject Management** - Organize classes, subjects, and teacher assignments
- ✅ **Weekly Schedule** - Visual timetable with lesson times and breaks
- ✅ **Attendance Tracking** - Daily attendance with multiple status options
- ✅ **Grade Management** - 1-5 grading system with statistics
- ✅ **Lesson Plans** - Weekly lesson planning with dates and homework
- ✅ **Notifications** - Send announcements to students by class or individually
- ✅ **Holiday Management** - Schedule holidays with 1-week advance alerts

### 🔴 Live Lesson Widget
- Real-time current lesson display
- Progress bar showing lesson completion
- Break time notifications
- Next lesson preview with homework
- **Voice Notifications** (Text-to-Speech)
  - "Matematika dersi başlandy" (Lesson started)
  - "Arakesme wagty" (Break time)
- Toggle sound on/off

### 📱 Mobile-Responsive
- Optimized for desktop, tablet, and mobile
- Touch-friendly interface
- Mobile menu with sidebar toggle
- Responsive tables and forms

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/edms.git
cd edms
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open browser**
```
http://localhost:5000
```

### Default Login
```
Username: director
Password: director123
```

## 📊 Database Schema

The system uses SQLite (development) or MySQL/PostgreSQL (production).

### Tables
- `users` - All system users (Director, Teacher, Student, Parent)
- `classes` - School classes with teacher assignments
- `subjects` - Subjects linked to classes and teachers
- `schedules` - Weekly lesson timetable
- `attendance` - Daily attendance records
- `grades` - Student grades with 1-5 scale
- `lesson_plans` - Weekly lesson plans with homework
- `notifications` - System notifications
- `holidays` - Holiday periods and breaks

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: SQLAlchemy ORM (SQLite/MySQL/PostgreSQL)
- **Authentication**: Flask-Login
- **Migrations**: Flask-Migrate
- **Security**: Werkzeug password hashing

### Frontend
- **Framework**: Bootstrap 5.3
- **Icons**: Bootstrap Icons 1.10
- **JavaScript**: Vanilla JS
- **Voice**: Web Speech API (Text-to-Speech)

## 📁 Project Structure

```
edms/
│
├── app.py                 # Main application file
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── edms.db               # SQLite database (auto-generated)
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── components/       # Reusable components
│   │   └── live_lesson_widget.html
│   ├── director/         # Director pages
│   ├── teacher/          # Teacher pages
│   ├── student/          # Student pages
│   └── parent/           # Parent pages
│
└── static/               # Static files
    ├── css/
    ├── js/
    └── images/
```

## 🎨 Screenshots

### Director Dashboard
Complete control panel with statistics and user management.

### Teacher Dashboard
Track attendance, manage grades, and create lesson plans.

### Student Dashboard
View schedules, grades, and receive notifications.

### Live Lesson Widget
Real-time lesson tracking with voice notifications.

## 🔧 Configuration

### Database Configuration
Edit `app.py`:

```python
# SQLite (default)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edms.db'

# MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/edms'

# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/edms'
```

### Secret Key
Change the secret key in production:

```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

## 🌐 Deployment

### Option 1: Render.com
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
git push render main
```

### Option 2: PythonAnywhere
1. Upload files to PythonAnywhere
2. Create virtual environment
3. Configure WSGI file
4. Reload web app

### Option 3: Railway
```bash
railway login
railway init
railway up
```

## 📖 User Guide

### For Directors
1. Create classes and subjects
2. Add teachers and assign to subjects
3. Create students and assign to classes
4. Build weekly schedules
5. Manage holidays and notifications

### For Teachers
1. View your daily schedule
2. Mark student attendance
3. Enter grades
4. Create lesson plans
5. Send notifications to students

### For Students
1. Check your daily schedule
2. View your grades
3. Read notifications
4. Track attendance
5. See homework assignments

### For Parents
1. View children's grades
2. Monitor attendance
3. Check progress reports

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- Voice notifications require browser support for Web Speech API
- Mobile sidebar may need manual close on some devices

## 🔮 Future Enhancements

- [ ] Dark mode
- [ ] File upload for homework submissions
- [ ] Real-time chat between teachers and students
- [ ] Email notifications
- [ ] SMS integration
- [ ] Mobile app (React Native)
- [ ] REST API
- [ ] Exam management
- [ ] Library management
- [ ] Fee management
- [ ] Report card generation (PDF)
- [ ] Multi-language support

## 👨‍💻 Author

**Your Name**
- GitHub: [@Kerim-N](https://github.com/Kerim-N)
- Email: nuryyewkerim123@gmail.com

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ for Education in Turkmenistan**
