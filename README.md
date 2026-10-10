# 🎓 Student and Teacher Management ERP System

A modern, secure, and production-ready Web-based Academic Enterprise Resource Planning (ERP) platform built with **Python Flask**, **MySQL / SQLite**, **SQLAlchemy ORM**, **Bootstrap 5**, **Chart.js**, and **ReportLab**.

Developed for universities, colleges, and schools to streamline student management, faculty attendance tracking, digital libraries, online timed MCQ tests, assignment workflows, automated grading, and PDF report cards.

---

## 🌟 Key Modules & Features

### 1. 🔐 Role-Based Authentication & Access Control
- **Three Core Roles**: Administrator, Teacher, and Student.
- Password hashing with Werkzeug security.
- Session management, "Remember Me" option, and eye-icon password toggle.
- Automatic role-based redirection to dedicated dashboards.

### 2. 📊 Executive Dashboards
- **Admin Dashboard**: Real-time KPI statistics cards (Total Students, Faculty, Classes, Subjects, Notes, Books, Today's Attendance %, Average Marks), 7-day attendance trend line charts via Chart.js, recent audit activity logs, and campus circulars.
- **Teacher Dashboard**: One-click daily biometric punch check-in/check-out with automatic working hours tracking, assigned classes/subjects, and rapid action shortcuts.
- **Student Dashboard**: Attendance ratio standing with **< 75% Short Attendance Warning Alert**, active tests with "Take Quiz" CTA, downloadable PDF report cards, and lecture notes.

### 3. 👥 Student & Faculty Management
- **Student Directory**: Add, edit, deactivate, and view student profiles with unique generated student UIDs (e.g., `STU-CS2301`).
- **CSV Data Processing**: One-click bulk export and import of student cohorts via CSV.
- **Teacher Directory**: Employee IDs, department assignments, designations, qualifications, and class in-charge assignments.

### 4. 📅 Smart Student & Teacher Attendance Registers
- **Student Attendance**:
  - Filter by Class, Section, Subject, and Date.
  - One-Click **"Mark All Present"** and **"Mark All Absent"** buttons.
  - Multi-status tracking: `Present`, `Absent`, `Late`, `Leave`.
  - Database unique constraint preventing accidental duplicate marks on the same day.
  - Attendance % computation: `(Attended / Held) * 100` with visual progress indicators and warnings.
  - CSV attendance report exports.
- **Teacher Attendance**:
  - Punch Check-In and Check-Out with automatic timestamps.
  - Calculates daily working hours.
  - Admin audit override log with accountability notes.

### 5. 📚 Study Notes & Digital Book Library
- **Study Notes**:
  - Upload lecture notes in PDF, DOC, DOCX, PPT, PPTX, or TXT format (up to 30 MB).
  - Target specific classes and subjects with chapter and topic metadata.
  - Instant in-app downloads.
- **Digital Library**:
  - Visual book card catalog with ISBN, publisher, publication year, and category tags.
  - Read/download authorized curriculum eBooks.

### 6. 📝 Timed Online Quizzes & Question Banks
- Create online objective tests with custom durations, passing scores, and instructions.
- Add MCQs with multiple options and automatic correct answer validation.
- **Real-Time Countdown Timer** for students with instant auto-submit when time expires.
- Instant automatic scoring and submission logs for instructors.

### 7. 🏆 Assessments, Marks Entry & PDF Report Cards
- Enter examination marks (Mid-Term, Final, Unit Tests, Practicals) with maximum score validation.
- Automatic computation of percentage and letter grades (`A+`, `A`, `B+`, `B`, `C`, `D`, `F`, `AB`).
- Toggle publish/unpublish to control visibility to students.
- **Official PDF Report Card Generation**: Powered by **ReportLab**, producing print-ready academic transcripts complete with institution header, subject marks breakdown, percentage, result status, and signature seals.

### 8. 💼 Assignments & Homework Submissions
- Teachers post assignments with deadlines, problem statements, and document attachments.
- Students upload solution files or write text answers.
- Submission tracking (`Submitted`, `Late`, `Evaluated`).
- Teachers evaluate and return grades with constructive feedback.

### 9. 📢 Notices, Notifications & Audit Security
- Campus-wide announcements broadcasted with urgency indicators (`Urgent`, `Exam`, `Holiday`, `General`).
- In-app notification center for deadlines, uploads, and grade releases.
- Audit logging of all critical administrative actions and IP addresses.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.10+, Flask 3.0+, Flask-Login, Werkzeug |
| **Database** | MySQL 8.0+ / SQLite 3 (Dual-Engine Support via SQLAlchemy 3.1+) |
| **Data Processing & PDF** | ReportLab 4+, Pandas 2.2+, OpenPyXL |
| **Frontend UI** | HTML5, CSS3 (Custom Design System), JavaScript ES6+ |
| **Styling & Frameworks** | Bootstrap 5.3, Font Awesome 6.5, Chart.js 4.4 |
| **Typography** | Plus Jakarta Sans, Space Grotesk |

---

## 🚀 Quick Start Guide (Windows)

### 1. Prerequisites
- Python 3.10 or higher installed.
- Git installed.

### 2. Clone / Open Repository
```powershell
cd D:\Student_Teacher_Attendance_ERP
```

### 3. Install Dependencies
```powershell
py -m pip install -r requirements.txt
```

### 4. Run the Application
```powershell
python app.py
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

*Note: On the first launch, the database and realistic demo accounts are initialized and seeded automatically!*

---

## 🔑 Demo Login Accounts

Use these pre-configured accounts or click the **1-Click Demo Buttons** on the login page:

| Role | Email / Identifier | Password | Access Rights |
|---|---|---|---|
| **Administrator** | `admin@example.com` | `Admin@12345` | Complete institutional ERP control |
| **Teacher** | `teacher@example.com` | `Teacher@12345` | Attendance, notes, quizzes, marks, grading |
| **Student** | `student@example.com` (or `CS2301`) | `Student@12345` | Attendance ratio, quiz tests, report cards |

---

## 🗄️ MySQL Database Setup (Optional Production Configuration)

By default, the ERP uses local SQLite (`student_erp.db`) with zero setup needed. To connect to a live MySQL server:

1. Open MySQL CLI or phpMyAdmin and execute:
```sql
CREATE DATABASE student_erp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
*(Or import the complete schema from [schema.sql](file:///d:/Student_Teacher_Attendance_ERP/schema.sql)).*

2. Create a `.env` file or set the environment variable:
```powershell
$env:DATABASE_URL="mysql+pymysql://YOUR_USER:YOUR_PASSWORD@127.0.0.1:3306/student_erp?charset=utf8mb4"
python app.py
```

---

## 🧪 Automated Testing

Run the test suite covering authentication, database seeding, grade calculations, and PDF generation:
```powershell
py -m unittest tests/test_app.py
```

---

## 🐙 Uploading to GitHub

To push this project to your GitHub account:

1. Create a new repository on [GitHub](https://github.com/new) (e.g. `Student-Teacher-Attendance-ERP`).
2. Run the following commands in PowerShell:

```powershell
# 1. Stage all project files
git add .

# 2. Create the initial commit
git commit -m "feat: complete student and teacher attendance ERP system with PDF report cards and online tests"

# 3. Rename branch to main
git branch -M main

# 4. Link your remote GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/Student-Teacher-Attendance-ERP.git

# 5. Push to GitHub
git push -u origin main
```

---

## 📄 License
This project is licensed under the MIT License - open for educational and institutional deployment.
