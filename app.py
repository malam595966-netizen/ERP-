import os
from datetime import date, datetime, timedelta
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from config import config
from models import (
    db, User, StudentProfile, TeacherProfile, Department, Course,
    Semester, ClassRoom, Subject, AcademicSession, StudentAttendance,
    TeacherAttendance, StudyNote, Book, Test, TestQuestion, TestOption,
    Assessment, StudentMark, Assignment, Announcement, Notification
)

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure upload directories exist
    upload_base = app.config["UPLOAD_FOLDER"]
    for folder in ["notes", "books", "assignments", "submissions", "profiles"]:
        os.makedirs(os.path.join(upload_base, folder), exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Context processors
    @app.context_processor
    def inject_global_vars():
        unread_count = 0
        if current_user.is_authenticated:
            unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        return {
            "institution_name": app.config.get("INSTITUTION_NAME", "Apex Institute ERP"),
            "current_year": datetime.now().year,
            "today_date": date.today(),
            "unread_notifications_count": unread_count
        }

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.students import students_bp
    from routes.teachers import teachers_bp
    from routes.academics import academics_bp
    from routes.attendance import attendance_bp
    from routes.materials import materials_bp
    from routes.exams import exams_bp
    from routes.marks import marks_bp
    from routes.assignments import assignments_bp
    from routes.notifications import notifications_bp
    from routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(academics_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(materials_bp)
    app.register_blueprint(exams_bp)
    app.register_blueprint(marks_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(reports_bp)

    # Error handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("error.html", code=403, title="Access Forbidden", message="You do not have administrative permission to view this resource."), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("error.html", code=404, title="Page Not Found", message="The requested page or record could not be found."), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("error.html", code=500, title="Server Error", message="An unexpected error occurred on the server. Please try again later."), 500

    return app

def seed_database(app):
    """Populates realistic initial academic and user demo records if database is empty."""
    with app.app_context():
        db.create_all()

        if User.query.count() > 0:
            return  # Already seeded

        print("Initializing realistic demo data for Student & Teacher ERP...")

        # 1. Departments
        cse = Department(name="Computer Science & Engineering", code="CSE", description="Department of CSE & AI")
        ece = Department(name="Electronics & Communication", code="ECE", description="Department of ECE & VLSI")
        me = Department(name="Mechanical Engineering", code="ME", description="Department of Mechanical Engineering")
        db.session.add_all([cse, ece, me])
        db.session.commit()

        # 2. Courses
        btech_cse = Course(name="B.Tech Computer Science", code="BTECH-CSE", department=cse, duration_years=4)
        btech_ece = Course(name="B.Tech Electronics", code="BTECH-ECE", department=ece, duration_years=4)
        db.session.add_all([btech_cse, btech_ece])
        db.session.commit()

        # 3. Semesters
        semesters = [Semester(number=i, name=f"Semester {i}") for i in range(1, 9)]
        db.session.add_all(semesters)
        db.session.commit()

        # 4. Users (Admin, Teachers, Students)
        # Admin
        admin = User(name="Principal / Director", email="admin@example.com", role="admin", phone="+91 9876543210")
        admin.set_password("Admin@12345")
        db.session.add(admin)

        # Teachers
        prof_sharma = User(name="Dr. Rajesh Sharma", email="teacher@example.com", role="teacher", phone="+91 9811122233")
        prof_sharma.set_password("Teacher@12345")
        prof_verma = User(name="Prof. Ananya Verma", email="ananya.verma@example.com", role="teacher", phone="+91 9822233344")
        prof_verma.set_password("Teacher@12345")

        db.session.add_all([prof_sharma, prof_verma])
        db.session.commit()

        t_prof1 = TeacherProfile(user=prof_sharma, employee_id="EMP-CSE-001", department=cse, designation="Associate Professor", qualification="Ph.D. in Computer Science")
        t_prof2 = TeacherProfile(user=prof_verma, employee_id="EMP-CSE-002", department=cse, designation="Assistant Professor", qualification="M.Tech Software Engineering")
        db.session.add_all([t_prof1, t_prof2])
        db.session.commit()

        # 5. Classes
        class_cse_3a = ClassRoom(name="B.Tech CSE 3rd Year", section="A", department=cse, course=btech_cse, semester=semesters[4], teacher_in_charge=prof_sharma)
        class_cse_3b = ClassRoom(name="B.Tech CSE 3rd Year", section="B", department=cse, course=btech_cse, semester=semesters[4], teacher_in_charge=prof_verma)
        db.session.add_all([class_cse_3a, class_cse_3b])
        db.session.commit()

        # 6. Subjects
        sub_dbms = Subject(name="Database Management Systems", code="CS-501", classroom=class_cse_3a, teacher=prof_sharma, credits=4)
        sub_os = Subject(name="Operating Systems", code="CS-502", classroom=class_cse_3a, teacher=prof_verma, credits=4)
        sub_web = Subject(name="Web Technologies & Cloud", code="CS-503", classroom=class_cse_3a, teacher=prof_sharma, credits=3)
        db.session.add_all([sub_dbms, sub_os, sub_web])
        db.session.commit()

        # 7. Students
        demo_students_data = [
            ("Aarav Mehta", "student@example.com", "CS2301", "Student@12345", "+91 9900112233", "Ramesh Mehta"),
            ("Diya Patel", "diya.patel@example.com", "CS2302", "Student@12345", "+91 9900112234", "Kishore Patel"),
            ("Rohan Gupta", "rohan.gupta@example.com", "CS2303", "Student@12345", "+91 9900112235", "Suresh Gupta"),
            ("Sneha Rao", "sneha.rao@example.com", "CS2304", "Student@12345", "+91 9900112236", "Venkatesh Rao"),
            ("Kavya Singh", "kavya.singh@example.com", "CS2305", "Student@12345", "+91 9900112237", "Mahesh Singh")
        ]

        created_students = []
        for s_name, s_email, s_roll, s_pass, s_phone, s_guardian in demo_students_data:
            s_user = User(name=s_name, email=s_email, role="student", phone=s_phone)
            s_user.set_password(s_pass)
            db.session.add(s_user)
            db.session.commit()

            s_prof = StudentProfile(
                user=s_user,
                student_uid=f"STU-{s_roll}",
                roll_number=s_roll,
                classroom=class_cse_3a,
                department=cse,
                dob=date(2004, 5, 15),
                address="University Campus Hostel A, Room 304",
                guardian_name=s_guardian,
                guardian_phone=s_phone
            )
            db.session.add(s_prof)
            created_students.append(s_user)
        db.session.commit()

        # 8. Student Attendance Seed (Past 5 days)
        today = date.today()
        for offset in range(5, -1, -1):
            att_date = today - timedelta(days=offset)
            for idx, stu in enumerate(created_students):
                # Make 1 student occasionally absent/late to show realistic stats
                if idx == 2 and offset in (1, 3):
                    status = "Absent"
                elif idx == 4 and offset == 2:
                    status = "Late"
                else:
                    status = "Present"

                sa = StudentAttendance(
                    student_id=stu.id,
                    class_id=class_cse_3a.id,
                    subject_id=sub_dbms.id,
                    attendance_date=att_date,
                    status=status,
                    marked_by_id=prof_sharma.id
                )
                db.session.add(sa)

        # 9. Teacher Attendance Seed
        for offset in range(4, -1, -1):
            att_date = today - timedelta(days=offset)
            ta = TeacherAttendance(
                teacher_id=prof_sharma.id,
                attendance_date=att_date,
                check_in=datetime.combine(att_date, datetime.min.time()).replace(hour=8, minute=45),
                check_out=datetime.combine(att_date, datetime.min.time()).replace(hour=16, minute=30),
                working_hours=7.75,
                status="Present"
            )
            db.session.add(ta)

        # 10. Study Notes Seed
        note1 = StudyNote(
            title="Relational Algebra & Normalization (1NF to BCNF)",
            description="Comprehensive lecture notes with solved decomposition examples.",
            subject_id=sub_dbms.id,
            class_id=class_cse_3a.id,
            chapter="Chapter 3: Relational Design",
            topic="Functional Dependencies and Decomposition",
            filename="sample_dbms_normalization.txt",
            original_filename="DBMS_Normalization_Lecture.pdf",
            file_size="1.8 MB",
            uploaded_by_id=prof_sharma.id
        )
        note2 = StudyNote(
            title="CPU Scheduling Algorithms & Deadlock Prevention",
            description="Detailed breakdown of Round Robin, SJF, and Banker's Algorithm.",
            subject_id=sub_os.id,
            class_id=class_cse_3a.id,
            chapter="Chapter 4: Process Scheduling",
            topic="Banker's Algorithm & Semaphore synchronization",
            filename="sample_os_scheduling.txt",
            original_filename="OS_CPU_Scheduling_Guide.pdf",
            file_size="2.4 MB",
            uploaded_by_id=prof_verma.id
        )
        db.session.add(note1)
        db.session.add(note2)
        db.session.commit()

        # Create dummy physical files for the notes so downloads work immediately
        notes_dir = os.path.join(app.config["UPLOAD_FOLDER"], "notes")
        os.makedirs(notes_dir, exist_ok=True)
        with open(os.path.join(notes_dir, "sample_dbms_normalization.txt"), "w") as f:
            f.write("DBMS Normalization Lecture Notes\n1NF: Atomic values\n2NF: No partial dependency\n3NF: No transitive dependency\nBCNF: Strict determinant rule.\n")
        with open(os.path.join(notes_dir, "sample_os_scheduling.txt"), "w") as f:
            f.write("Operating Systems Lecture Notes\nProcess Scheduling:\n1. FCFS\n2. Round Robin\n3. Shortest Job First\nDeadlock conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.\n")

        # 11. Digital Books Seed
        book1 = Book(
            title="Database System Concepts (7th Edition)",
            author="Abraham Silberschatz, Henry Korth, S. Sudarshan",
            isbn="978-0078022159",
            publisher="McGraw-Hill Education",
            pub_year=2020,
            category="Computer Science",
            description="The premier standard textbook for foundational database concepts and relational calculus.",
            availability_status="Available",
            uploaded_by_id=admin.id
        )
        book2 = Book(
            title="Modern Operating Systems (4th Edition)",
            author="Andrew S. Tanenbaum, Herbert Bos",
            isbn="978-0133591620",
            publisher="Pearson",
            pub_year=2015,
            category="Systems Engineering",
            description="Classic reference for processes, virtualization, memory management, and modern kernel architectures.",
            availability_status="Available",
            uploaded_by_id=admin.id
        )
        db.session.add(book1)
        db.session.add(book2)
        db.session.commit()

        # 12. Assessment & Marks Seed
        asmt1 = Assessment(
            title="Mid-Semester Exam: DBMS",
            subject_id=sub_dbms.id,
            class_id=class_cse_3a.id,
            assessment_type="Mid-Term",
            max_marks=100.0,
            passing_marks=40.0,
            is_published=True,
            created_by_id=prof_sharma.id
        )
        asmt2 = Assessment(
            title="Unit Test 1: Operating Systems",
            subject_id=sub_os.id,
            class_id=class_cse_3a.id,
            assessment_type="Unit Test",
            max_marks=50.0,
            passing_marks=20.0,
            is_published=True,
            created_by_id=prof_verma.id
        )
        db.session.add(asmt1)
        db.session.add(asmt2)
        db.session.commit()

        # Seed Marks
        student_scores = [92.0, 85.5, 74.0, 88.0, 68.5]
        for idx, stu in enumerate(created_students):
            m1 = StudentMark(
                assessment_id=asmt1.id,
                student_id=stu.id,
                obtained_marks=student_scores[idx],
                is_absent=False,
                remarks="Consistent performance",
                entered_by_id=prof_sharma.id
            )
            m1.calculate_grade(asmt1.max_marks)
            db.session.add(m1)

            m2 = StudentMark(
                assessment_id=asmt2.id,
                student_id=stu.id,
                obtained_marks=round(student_scores[idx] / 2, 1),
                is_absent=False,
                remarks="Good conceptual clarity",
                entered_by_id=prof_verma.id
            )
            m2.calculate_grade(asmt2.max_marks)
            db.session.add(m2)

        # 13. Online Test (MCQ) Seed
        test1 = Test(
            title="DBMS Online Practice Quiz",
            subject=sub_dbms,
            classroom=class_cse_3a,
            duration_minutes=15,
            total_marks=10.0,
            passing_marks=4.0,
            instructions="Attempt all questions. 2 marks per question. Timer will auto-submit when done.",
            test_type="mcq",
            is_published=True,
            created_by_id=prof_sharma.id
        )
        db.session.add(test1)
        db.session.commit()

        q1 = TestQuestion(test_id=test1.id, question_text="Which of the following normal forms eliminates transitive functional dependencies?", marks=2.0, order_num=1)
        db.session.add(q1); db.session.flush()
        db.session.add_all([
            TestOption(question_id=q1.id, option_text="First Normal Form (1NF)", is_correct=False),
            TestOption(question_id=q1.id, option_text="Second Normal Form (2NF)", is_correct=False),
            TestOption(question_id=q1.id, option_text="Third Normal Form (3NF)", is_correct=True),
            TestOption(question_id=q1.id, option_text="None of the above", is_correct=False)
        ])

        q2 = TestQuestion(test_id=test1.id, question_text="What SQL statement is used to remove a table definition and all its data?", marks=2.0, order_num=2)
        db.session.add(q2); db.session.flush()
        db.session.add_all([
            TestOption(question_id=q2.id, option_text="DROP TABLE", is_correct=True),
            TestOption(question_id=q2.id, option_text="DELETE TABLE", is_correct=False),
            TestOption(question_id=q2.id, option_text="TRUNCATE", is_correct=False),
            TestOption(question_id=q2.id, option_text="REMOVE TABLE", is_correct=False)
        ])

        # 14. Announcement Seed
        ann1 = Announcement(
            title="Mid-Term Examination Schedule & Attendance Notice",
            content="Students are reminded that a minimum of 75% attendance is required to sit for the upcoming university examinations.",
            priority="urgent",
            target_role="all",
            created_by_id=admin.id
        )
        ann2 = Announcement(
            title="Annual Tech Symposium & Hackathon Registration",
            content="Registration is now open for Apex Hack 2026. Submit project proposals before the end of the month.",
            priority="general",
            target_role="student",
            created_by_id=admin.id
        )
        db.session.add_all([ann1, ann2])

        db.session.commit()
        print("Demo data seeded successfully with Admin, Teachers, and Students!")

app = create_app()

if __name__ == "__main__":
    seed_database(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
