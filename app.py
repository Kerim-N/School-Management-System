from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
from datetime import datetime
app.jinja_env.globals['now'] = datetime.now
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import and initialize database
from models import db, User, Class, Subject, LessonPlan, Attendance, Grade, Message, Schedule, Notification, Holiday
db.init_app(app)

# Initialize extensions
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bu sahypa görmek üçin giriň'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'director':
            return redirect(url_for('director_dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student_dashboard'))
        elif current_user.role == 'parent':
            return redirect(url_for('parent_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Ulanyjy ady ýa-da parol nädogry', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Siz ulgamdan çykdyňyz', 'info')
    return redirect(url_for('login'))

# Director Routes
@app.route('/director/dashboard')
@login_required
def director_dashboard():
    if current_user.role != 'director':
        flash('Siziň bu sahypa girmäge hukugyňyz ýok', 'danger')
        return redirect(url_for('index'))
    
    stats = {
        'total_students': User.query.filter_by(role='student').count(),
        'total_teachers': User.query.filter_by(role='teacher').count(),
        'total_classes': Class.query.count(),
        'total_subjects': Subject.query.count()
    }
    
    return render_template('director/dashboard.html', stats=stats)

@app.route('/director/users')
@login_required
def director_users():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('director/users.html', users=users)

@app.route('/director/user/create', methods=['GET', 'POST'])
@login_required
def director_create_user():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        class_id = request.form.get('class_id')
        
        if User.query.filter_by(username=username).first():
            flash('Bu ulanyjy ady eýýäm bar', 'danger')
            return redirect(url_for('director_create_user'))
        
        user = User(
            username=username,
            password=generate_password_hash(password),
            full_name=full_name,
            role=role,
            class_id=int(class_id) if class_id else None
        )
        
        db.session.add(user)
        db.session.commit()
        flash('Täze ulanyjy döredildi', 'success')
        return redirect(url_for('director_users'))
    
    classes = Class.query.all()
    return render_template('director/create_user.html', classes=classes)

@app.route('/director/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def director_edit_user(user_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.full_name = request.form.get('full_name')
        user.role = request.form.get('role')
        class_id = request.form.get('class_id')
        user.class_id = int(class_id) if class_id else None
        
        new_password = request.form.get('new_password')
        if new_password:
            user.password = generate_password_hash(new_password)
        
        db.session.commit()
        flash('Ulanyjy maglumatlar täzelendi', 'success')
        return redirect(url_for('director_users'))
    
    classes = Class.query.all()
    return render_template('director/edit_user.html', user=user, classes=classes)

@app.route('/director/user/delete/<int:user_id>', methods=['POST'])
@login_required
def director_delete_user(user_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Ulanyjy öçürildi', 'success')
    return redirect(url_for('director_users'))

@app.route('/director/classes')
@login_required
def director_classes():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    classes = Class.query.all()
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('director/classes.html', classes=classes, teachers=teachers)

@app.route('/director/class/create', methods=['POST'])
@login_required
def director_create_class():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    name = request.form.get('name')
    teacher_id = request.form.get('teacher_id')
    
    new_class = Class(
        name=name,
        teacher_id=int(teacher_id) if teacher_id else None
    )
    
    db.session.add(new_class)
    db.session.commit()
    flash('Täze synp döredildi', 'success')
    return redirect(url_for('director_classes'))

@app.route('/director/subjects')
@login_required
def director_subjects():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    subjects = Subject.query.all()
    classes = Class.query.all()
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('director/subjects.html', subjects=subjects, classes=classes, teachers=teachers)

@app.route('/director/subject/create', methods=['POST'])
@login_required
def director_create_subject():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    name = request.form.get('name')
    class_id = request.form.get('class_id')
    teacher_id = request.form.get('teacher_id')
    
    subject = Subject(
        name=name,
        class_id=int(class_id),
        teacher_id=int(teacher_id)
    )
    
    db.session.add(subject)
    db.session.commit()
    flash('Täze ders döredildi', 'success')
    return redirect(url_for('director_subjects'))

@app.route('/director/subject/delete/<int:subject_id>', methods=['POST'])
@login_required
def director_delete_subject(subject_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash('Ders öçürildi', 'success')
    return redirect(url_for('director_subjects'))

@app.route('/director/class/delete/<int:class_id>', methods=['POST'])
@login_required
def director_delete_class(class_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    class_obj = Class.query.get_or_404(class_id)
    db.session.delete(class_obj)
    db.session.commit()
    flash('Synp öçürildi', 'success')
    return redirect(url_for('director_classes'))

@app.route('/director/schedules')
@login_required
def director_schedules():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    classes = Class.query.all()
    return render_template('director/schedules.html', classes=classes)

@app.route('/director/schedule/<int:class_id>')
@login_required
def director_view_schedule(class_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    class_obj = Class.query.get_or_404(class_id)
    subjects = Subject.query.filter_by(class_id=class_id).all()
    schedules = Schedule.query.filter_by(class_id=class_id).order_by(Schedule.day_of_week, Schedule.lesson_number).all()
    
    # Organize schedules by day
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    schedule_by_day = {day: [] for day in days}
    
    for schedule in schedules:
        schedule_by_day[schedule.day_of_week].append(schedule)
    
    return render_template('director/view_schedule.html', 
                         class_obj=class_obj, 
                         subjects=subjects,
                         schedule_by_day=schedule_by_day,
                         days=days)

@app.route('/director/schedule/<int:class_id>/create', methods=['POST'])
@login_required
def director_create_schedule(class_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    day_of_week = request.form.get('day_of_week')
    lesson_number = request.form.get('lesson_number')
    subject_id = request.form.get('subject_id')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    
    schedule = Schedule(
        class_id=class_id,
        day_of_week=day_of_week,
        lesson_number=int(lesson_number),
        subject_id=int(subject_id),
        start_time=start_time,
        end_time=end_time
    )
    
    db.session.add(schedule)
    db.session.commit()
    flash('Ders jadwala goşuldy', 'success')
    return redirect(url_for('director_view_schedule', class_id=class_id))

@app.route('/director/schedule/delete/<int:schedule_id>', methods=['POST'])
@login_required
def director_delete_schedule(schedule_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    schedule = Schedule.query.get_or_404(schedule_id)
    class_id = schedule.class_id
    db.session.delete(schedule)
    db.session.commit()
    flash('Ders jadwaldan öçürildi', 'success')
    return redirect(url_for('director_view_schedule', class_id=class_id))

@app.route('/director/parents')
@login_required
def director_parents():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    parents = User.query.filter_by(role='parent').all()
    students = User.query.filter_by(role='student').all()
    return render_template('director/parents.html', parents=parents, students=students)

@app.route('/director/parent/<int:parent_id>/add-child', methods=['POST'])
@login_required
def director_add_child_to_parent(parent_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    student_id = request.form.get('student_id')
    student = User.query.get_or_404(student_id)
    student.parent_id = parent_id
    db.session.commit()
    flash('Çaga ene-ata baglandy', 'success')
    return redirect(url_for('director_parents'))

@app.route('/director/parent/<int:parent_id>/remove-child/<int:student_id>', methods=['POST'])
@login_required
def director_remove_child_from_parent(parent_id, student_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    student = User.query.get_or_404(student_id)
    student.parent_id = None
    db.session.commit()
    flash('Çaga ene-atadan aýryldy', 'success')
    return redirect(url_for('director_parents'))

@app.route('/director/holidays')
@login_required
def director_holidays():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    holidays = Holiday.query.order_by(Holiday.start_date.desc()).all()
    return render_template('director/holidays.html', holidays=holidays)

@app.route('/director/holiday/create', methods=['POST'])
@login_required
def director_create_holiday():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    description = request.form.get('description')
    
    holiday = Holiday(
        name=name,
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
        description=description
    )
    
    db.session.add(holiday)
    db.session.commit()
    flash('Baýramçylyk döredildi', 'success')
    return redirect(url_for('director_holidays'))

@app.route('/director/holiday/delete/<int:holiday_id>', methods=['POST'])
@login_required
def director_delete_holiday(holiday_id):
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    holiday = Holiday.query.get_or_404(holiday_id)
    db.session.delete(holiday)
    db.session.commit()
    flash('Baýramçylyk öçürildi', 'success')
    return redirect(url_for('director_holidays'))

@app.route('/director/notifications')
@login_required
def director_notifications():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    students = User.query.filter_by(role='student').all()
    classes = Class.query.all()
    return render_template('director/notifications.html', students=students, classes=classes)

@app.route('/director/send-notification', methods=['POST'])
@login_required
def director_send_notification():
    if current_user.role != 'director':
        return redirect(url_for('index'))
    
    receiver_type = request.form.get('receiver_type')
    title = request.form.get('title')
    message = request.form.get('message')
    
    receivers = []
    
    if receiver_type == 'all_students':
        receivers = User.query.filter_by(role='student').all()
    elif receiver_type == 'class':
        class_id = request.form.get('class_id')
        receivers = User.query.filter_by(role='student', class_id=int(class_id)).all()
    elif receiver_type == 'individual':
        student_id = request.form.get('student_id')
        receivers = [User.query.get(int(student_id))]
    
    for receiver in receivers:
        notification = Notification(
            sender_id=current_user.id,
            receiver_id=receiver.id,
            title=title,
            message=message
        )
        db.session.add(notification)
    
    db.session.commit()
    flash(f'{len(receivers)} okuwça bildirim iberildi', 'success')
    return redirect(url_for('director_notifications'))

# Teacher Routes
@app.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    my_classes = Class.query.filter_by(teacher_id=current_user.id).all()
    my_subjects = Subject.query.filter_by(teacher_id=current_user.id).all()
    
    # Get current lesson info
    from datetime import date, timedelta
    today = date.today()
    day_name = today.strftime('%A')
    
    subject_ids = [s.id for s in my_subjects]
    schedules = Schedule.query.filter(
        Schedule.subject_id.in_(subject_ids),
        Schedule.day_of_week == day_name
    ).order_by(Schedule.lesson_number).all()
    
    # Convert to JSON-serializable format
    current_schedule = []
    for schedule in schedules:
        current_schedule.append({
            'id': schedule.id,
            'lesson_number': schedule.lesson_number,
            'start_time': schedule.start_time,
            'end_time': schedule.end_time,
            'subject': {
                'id': schedule.subject.id,
                'name': schedule.subject.name,
                'teacher': {
                    'id': schedule.subject.teacher.id,
                    'full_name': schedule.subject.teacher.full_name
                }
            },
            'class': {
                'id': schedule.class_obj.id,
                'name': schedule.class_obj.name
            }
        })
    
    # Check for upcoming holidays
    one_week_later = today + timedelta(days=7)
    upcoming_holidays = Holiday.query.filter(
        Holiday.start_date >= today,
        Holiday.start_date <= one_week_later
    ).all()
    
    return render_template('teacher/dashboard.html', 
                         classes=my_classes, 
                         subjects=my_subjects,
                         current_schedule=current_schedule,
                         upcoming_holidays=upcoming_holidays)

@app.route('/teacher/students')
@login_required
def teacher_students():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    my_classes = Class.query.filter_by(teacher_id=current_user.id).all()
    class_ids = [c.id for c in my_classes]
    students = User.query.filter(User.role == 'student', User.class_id.in_(class_ids)).all()
    
    return render_template('teacher/students.html', students=students)

@app.route('/teacher/attendance', methods=['GET', 'POST'])
@login_required
def teacher_attendance():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        date = request.form.get('date')
        student_ids = request.form.getlist('student_ids')
        
        for student_id in student_ids:
            status = request.form.get(f'status_{student_id}')
            attendance = Attendance(
                student_id=int(student_id),
                date=datetime.strptime(date, '%Y-%m-%d'),
                status=status
            )
            db.session.add(attendance)
        
        db.session.commit()
        flash('Gatnaşyk bellenildi', 'success')
        return redirect(url_for('teacher_attendance'))
    
    my_classes = Class.query.filter_by(teacher_id=current_user.id).all()
    class_ids = [c.id for c in my_classes]
    students = User.query.filter(User.role == 'student', User.class_id.in_(class_ids)).all()
    
    return render_template('teacher/attendance.html', students=students)

@app.route('/teacher/grades', methods=['GET', 'POST'])
@login_required
def teacher_grades():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject_id = request.form.get('subject_id')
        grade_value = request.form.get('grade')
        
        grade = Grade(
            student_id=int(student_id),
            subject_id=int(subject_id),
            grade=int(grade_value),
            date=datetime.now()
        )
        db.session.add(grade)
        db.session.commit()
        flash('Baha girizildi', 'success')
        return redirect(url_for('teacher_grades'))
    
    my_subjects = Subject.query.filter_by(teacher_id=current_user.id).all()
    my_classes = Class.query.filter_by(teacher_id=current_user.id).all()
    class_ids = [c.id for c in my_classes]
    students = User.query.filter(User.role == 'student', User.class_id.in_(class_ids)).all()
    
    # Get all grades for teacher's subjects
    subject_ids = [s.id for s in my_subjects]
    all_grades = Grade.query.filter(Grade.subject_id.in_(subject_ids)).order_by(Grade.date.desc()).all()
    
    return render_template('teacher/grades.html', subjects=my_subjects, students=students, all_grades=all_grades)

@app.route('/teacher/lesson-plans')
@login_required
def teacher_lesson_plans():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    my_subjects = Subject.query.filter_by(teacher_id=current_user.id).all()
    subject_ids = [s.id for s in my_subjects]
    plans = LessonPlan.query.filter(LessonPlan.subject_id.in_(subject_ids)).all()
    
    return render_template('teacher/lesson_plans.html', plans=plans, subjects=my_subjects)

@app.route('/teacher/lesson-plan/create', methods=['POST'])
@login_required
def teacher_create_plan():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    subject_id = request.form.get('subject_id')
    week = request.form.get('week')
    date = request.form.get('date')
    topic = request.form.get('topic')
    objectives = request.form.get('objectives')
    homework = request.form.get('homework')
    
    plan = LessonPlan(
        subject_id=int(subject_id),
        week=int(week),
        date=datetime.strptime(date, '%Y-%m-%d').date() if date else None,
        topic=topic,
        objectives=objectives,
        homework=homework
    )
    
    db.session.add(plan)
    db.session.commit()
    flash('Okuw meýilnamasy döredildi', 'success')
    return redirect(url_for('teacher_lesson_plans'))

@app.route('/teacher/schedule')
@login_required
def teacher_schedule():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    # Get all classes where teacher is assigned
    my_classes = Class.query.filter_by(teacher_id=current_user.id).all()
    
    # Get schedules for teacher's subjects
    my_subjects = Subject.query.filter_by(teacher_id=current_user.id).all()
    subject_ids = [s.id for s in my_subjects]
    schedules = Schedule.query.filter(Schedule.subject_id.in_(subject_ids)).order_by(Schedule.day_of_week, Schedule.lesson_number).all()
    
    # Organize by day
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    schedule_by_day = {day: [] for day in days}
    
    for schedule in schedules:
        schedule_by_day[schedule.day_of_week].append(schedule)
    
    return render_template('teacher/schedule.html', schedule_by_day=schedule_by_day, days=days)

@app.route('/teacher/notifications')
@login_required
def teacher_notifications():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    my_classes = Class.query.filter_by(teacher_id=current_user.id).all()
    class_ids = [c.id for c in my_classes]
    students = User.query.filter(User.role == 'student', User.class_id.in_(class_ids)).all()
    
    return render_template('teacher/notifications.html', students=students, my_classes=my_classes)

@app.route('/teacher/send-notification', methods=['POST'])
@login_required
def teacher_send_notification():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    receiver_type = request.form.get('receiver_type')
    title = request.form.get('title')
    message = request.form.get('message')
    
    receivers = []
    
    if receiver_type == 'class':
        class_id = request.form.get('class_id')
        receivers = User.query.filter_by(role='student', class_id=int(class_id)).all()
    elif receiver_type == 'individual':
        student_id = request.form.get('student_id')
        receivers = [User.query.get(int(student_id))]
    
    for receiver in receivers:
        notification = Notification(
            sender_id=current_user.id,
            receiver_id=receiver.id,
            title=title,
            message=message
        )
        db.session.add(notification)
    
    db.session.commit()
    flash(f'{len(receivers)} okuwça bildirim iberildi', 'success')
    return redirect(url_for('teacher_notifications'))

# Student Routes
@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    my_class = Class.query.get(current_user.class_id) if current_user.class_id else None
    subjects = Subject.query.filter_by(class_id=current_user.class_id).all() if current_user.class_id else []
    
    # Get current lesson info
    from datetime import date, timedelta
    today = date.today()
    day_name = today.strftime('%A')
    
    schedules = Schedule.query.filter(
        Schedule.class_id == current_user.class_id,
        Schedule.day_of_week == day_name
    ).order_by(Schedule.lesson_number).all() if current_user.class_id else []
    
    # Convert to JSON-serializable format
    current_schedule = []
    for schedule in schedules:
        current_schedule.append({
            'id': schedule.id,
            'lesson_number': schedule.lesson_number,
            'start_time': schedule.start_time,
            'end_time': schedule.end_time,
            'subject': {
                'id': schedule.subject.id,
                'name': schedule.subject.name,
                'teacher': {
                    'id': schedule.subject.teacher.id,
                    'full_name': schedule.subject.teacher.full_name
                }
            },
            'class': {
                'id': schedule.class_obj.id,
                'name': schedule.class_obj.name
            }
        })
    
    # Check for upcoming holidays
    one_week_later = today + timedelta(days=7)
    upcoming_holidays = Holiday.query.filter(
        Holiday.start_date >= today,
        Holiday.start_date <= one_week_later
    ).all()
    
    return render_template('student/dashboard.html', 
                         my_class=my_class, 
                         subjects=subjects,
                         current_schedule=current_schedule,
                         upcoming_holidays=upcoming_holidays)

@app.route('/student/grades')
@login_required
def student_grades():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    grades = Grade.query.filter_by(student_id=current_user.id).all()
    return render_template('student/grades.html', grades=grades)

@app.route('/student/attendance')
@login_required
def student_attendance():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    attendance = Attendance.query.filter_by(student_id=current_user.id).order_by(Attendance.date.desc()).all()
    return render_template('student/attendance.html', attendance=attendance)

@app.route('/student/lesson-plans')
@login_required
def student_lesson_plans():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    subjects = Subject.query.filter_by(class_id=current_user.class_id).all() if current_user.class_id else []
    subject_ids = [s.id for s in subjects]
    plans = LessonPlan.query.filter(LessonPlan.subject_id.in_(subject_ids)).all()
    
    return render_template('student/lesson_plans.html', plans=plans)

@app.route('/student/schedule')
@login_required
def student_schedule():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    if not current_user.class_id:
        flash('Sizä entek synp bellenmedi', 'warning')
        return redirect(url_for('student_dashboard'))
    
    schedules = Schedule.query.filter_by(class_id=current_user.class_id).order_by(Schedule.day_of_week, Schedule.lesson_number).all()
    
    # Organize by day
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    schedule_by_day = {day: [] for day in days}
    
    for schedule in schedules:
        schedule_by_day[schedule.day_of_week].append(schedule)
    
    return render_template('student/schedule.html', schedule_by_day=schedule_by_day, days=days)

@app.route('/student/notifications')
@login_required
def student_notifications():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    notifications = Notification.query.filter_by(receiver_id=current_user.id).order_by(Notification.created_at.desc()).all()
    
    return render_template('student/notifications.html', notifications=notifications)

@app.route('/student/notification/<int:notif_id>/read', methods=['POST'])
@login_required
def student_mark_notification_read(notif_id):
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    notification = Notification.query.get_or_404(notif_id)
    if notification.receiver_id == current_user.id:
        notification.is_read = True
        db.session.commit()
    
    return redirect(url_for('student_notifications'))

# Parent Routes
@app.route('/parent/dashboard')
@login_required
def parent_dashboard():
    if current_user.role != 'parent':
        return redirect(url_for('index'))
    
    children = User.query.filter_by(role='student', parent_id=current_user.id).all()
    return render_template('parent/dashboard.html', children=children)

@app.route('/parent/child/<int:child_id>/grades')
@login_required
def parent_child_grades(child_id):
    if current_user.role != 'parent':
        return redirect(url_for('index'))
    
    child = User.query.get_or_404(child_id)
    if child.parent_id != current_user.id:
        flash('Siziň bu sahypa girmäge hukugyňyz ýok', 'danger')
        return redirect(url_for('parent_dashboard'))
    
    grades = Grade.query.filter_by(student_id=child_id).all()
    return render_template('parent/child_grades.html', child=child, grades=grades)

@app.route('/parent/child/<int:child_id>/attendance')
@login_required
def parent_child_attendance(child_id):
    if current_user.role != 'parent':
        return redirect(url_for('index'))
    
    child = User.query.get_or_404(child_id)
    if child.parent_id != current_user.id:
        flash('Siziň bu sahypa girmäge hukugyňyz ýok', 'danger')
        return redirect(url_for('parent_dashboard'))
    
    attendance = Attendance.query.filter_by(student_id=child_id).order_by(Attendance.date.desc()).all()
    return render_template('parent/child_attendance.html', child=child, attendance=attendance)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default director if not exists
        if not User.query.filter_by(username='director').first():
            director = User(
                username='director',
                password=generate_password_hash('director123'),
                full_name='Direktor',
                role='director'
            )
            db.session.add(director)
            db.session.commit()
            print("✓ Default director created: username='director', password='director123'")
    
    app.run(host='0.0.0.0', port=5000, debug=False)