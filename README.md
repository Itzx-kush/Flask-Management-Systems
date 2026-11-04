# Flask Management Systems

A unified, production-grade Python Flask web application integrating all four mandatory practical questions from the Flask Laboratory curriculum into one cohesive platform with a single administrative dashboard, shared modern design system, and persistent SQLite database backend.

- **GitHub Repository:** [https://github.com/Itzx-kush/Flask-Management-Systems](https://github.com/Itzx-kush/Flask-Management-Systems)
- **Author / GitHub Owner:** [Itzx-kush](https://github.com/Itzx-kush) (Kusumakar Rokkam)
- **Local Address:** [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Implemented Practicals](#implemented-practicals)
   - [Practical 1: Student Management System Using Flask Forms](#practical-1--student-management-system-using-flask-forms)
   - [Practical 2: Hospital Appointment System Using Flask](#practical-2--hospital-appointment-system-using-flask)
   - [Practical 3: Student Information Management System Using Flask and SQLite](#practical-3--student-information-management-system-using-flask-and-sqlite)
   - [Practical 4: Employee Management System Using Flask and Database](#practical-4--employee-management-system-using-flask-and-database)
3. [Key Features & Design System](#key-features--design-system)
4. [Technology Stack](#technology-stack)
5. [Database Architecture](#database-architecture)
6. [Project Structure](#project-structure)
7. [Installation & Windows Execution](#installation--windows-execution)
8. [Running Automated Tests](#running-automated-tests)
9. [UI Screenshots & Previews](#ui-screenshots--previews)
10. [License & Academic Integrity](#license--academic-integrity)

---

## 1. Project Overview

Traditionally, academic laboratory assignments are executed as disparate single-script demonstrations running on varied ports. **Flask Management Systems** consolidates all four lab practicals into a single enterprise-styled administrative application.

Using **Flask Blueprints**, each practical operates as an independent module while sharing:
- A unified administrative layout and navigation sidebar.
- Consistent typography and blue/indigo primary color palette (`#2563eb`, `#4f46e5`).
- Cross-Site Request Forgery (CSRF) protection on all state-changing forms.
- Reusable SQLite database connections with parameterized query execution.
- Comprehensive in-app lab documentation (`/practicals`) with aims, algorithms, and results.

---

## 2. Implemented Practicals

### Practical 1 — Student Management System Using Flask Forms
- **Objective:** Accept student name and department details through a web form, validate inputs on the server, and render submitted details.
- **Workflow:** `HTML Form → Flask Route → Input Validation → Display Result`.
- **Validation Rules:**
  - Student Name: Non-empty, 2–60 characters, alphabetical characters, spaces, dots, or hyphens only.
  - Department: Non-empty selection from the approved list of academic departments.
- **Result Display:** Formats submitted student details, submission timestamp, and HTTP method badge without requiring database storage (stateless demonstration).

### Practical 2 — Hospital Appointment System Using Flask
- **Objective:** Accept patient consultation booking details, validate input data, prevent past date reservations, and generate an appointment confirmation slip.
- **Fields:** Patient Name, Doctor Selection (with medical specialization), Appointment Date, Contact Phone, and Email Address.
- **Validation Rules:**
  - Date Validation: Prevents booking appointments in the past (`appointment_date >= date.today()`).
  - Contact Validation: 10–15 digit phone format.
  - Email Validation: RFC-compliant email structure.
- **Confirmation Display:** Generates a unique tracking reference (e.g., `APT-YYYYMMDD-XXXX`), displays status `Confirmed`, and provides an academic laboratory notice.

### Practical 3 — Student Information Management System Using Flask and SQLite
- **Objective:** Complete database-driven CRUD application using SQLite with data persistence across server restarts.
- **Database Table:** `students`
- **CRUD Capabilities:**
  - **CREATE:** Add student form, validates fields, and strictly prevents duplicate roll numbers.
  - **READ:** Tabular directory with column sorting, profile detail card (`/students/<id>`), and search by name, roll number, or department (`/students?q=...`).
  - **UPDATE:** Pre-populated edit form, cross-record uniqueness validation (`roll_number = ? AND id != ?`), and confirmation update.
  - **DELETE:** Modal confirmation dialog preventing accidental deletions, executed via `POST /students/delete/<id>`.

### Practical 4 — Employee Management System Using Flask and Database
- **Objective:** Accept employee employment details, enforce unique corporate IDs, validate compensation, and display records in an administrative table.
- **Database Table:** `employees`
- **Capabilities:**
  - Form validation for Employee ID, Name, Department, Designation, Email, Phone, Salary (positive numeric check), and Joining Date.
  - Unique constraint enforcement preventing duplicate Employee IDs.
  - Interactive directory table with currency formatting (`${:,.2f}`) and live search by employee name or ID.
  - Full edit and delete management operations.

---

## 3. Key Features & Design System

- **Clean White & Slate Design:** Built on a clean background (`#f8fafc`) with royal blue and deep indigo accents.
- **Responsive Sidebar:** Collapsible off-canvas sidebar on mobile with hamburger toggle; sticky navigation on desktop.
- **Real-Time Search:** Server-side search filter with query persistence alongside client-side instant filtering.
- **Safe Modal Dialogs:** Custom JavaScript-driven deletion modals replacing crude browser prompts.
- **CSRF Token Security:** Session-based token generation and verification protecting all POST requests.
- **Flash Toast Alerts:** Auto-dismissing feedback notifications for successful creations, updates, and deletions.

---

## 4. Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3.10+ | Core language runtime |
| **Framework** | Flask 3.x | Web framework, request routing, blueprints |
| **Templates** | Jinja2 | Reusable layout inheritance and template rendering |
| **Database** | SQLite 3 | Embedded relational persistence engine (`instance/management.db`) |
| **Frontend** | HTML5, CSS3, JavaScript | Responsive UI, input masking, modal controller |
| **Testing** | Pytest 8.x / 9.x | Automated test runner with isolated temporary database |
| **VCS** | Git & GitHub | Version control and collaborative feature branching |

---

## 5. Database Architecture

The application persists data in SQLite located at `instance/management.db`. Tables are automatically created during startup if not present, ensuring that data persists seamlessly across application restarts.

```
instance/management.db
├── students
│   ├── id (INTEGER PRIMARY KEY AUTOINCREMENT)
│   ├── student_name (TEXT NOT NULL)
│   ├── roll_number (TEXT NOT NULL UNIQUE)
│   ├── department (TEXT NOT NULL)
│   ├── email (TEXT NOT NULL)
│   ├── phone (TEXT NOT NULL)
│   ├── semester (TEXT NOT NULL)
│   └── created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
│
└── employees
    ├── id (INTEGER PRIMARY KEY AUTOINCREMENT)
    ├── employee_id (TEXT NOT NULL UNIQUE)
    ├── employee_name (TEXT NOT NULL)
    ├── department (TEXT NOT NULL)
    ├── designation (TEXT NOT NULL)
    ├── email (TEXT NOT NULL)
    ├── phone (TEXT NOT NULL)
    ├── salary (REAL NOT NULL)
    ├── joining_date (TEXT NOT NULL)
    └── created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

---

## 6. Project Structure

```
Flask-Management-Systems/
├── app.py                      # Application factory, CSRF hook, error handlers
├── database.py                 # SQLite connection helper, table init, parameterized execution
├── config.py                   # Configuration classes (Dev & Test configs)
├── validators.py               # Reusable regex and form validation logic
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git exclusion rules
│
├── instance/
│   ├── .gitkeep                # Keeps instance directory in git
│   └── management.db           # SQLite database (auto-generated, gitignored)
│
├── routes/
│   ├── __init__.py             # Exports all modular blueprints
│   ├── dashboard.py            # Main landing dashboard routes (/ and /dashboard)
│   ├── student_form.py         # Practical 1: Form handling routes
│   ├── hospital.py             # Practical 2: Hospital appointment routes
│   ├── students.py             # Practical 3: Student SQLite CRUD routes
│   ├── employees.py            # Practical 4: Employee management routes
│   └── practicals.py           # Practical documentation and about pages
│
├── templates/
│   ├── base.html               # Shared master layout with sidebar & delete modal
│   ├── dashboard.html          # Main landing page with metric cards
│   ├── practicals.html         # Comprehensive lab documentation page
│   ├── about.html              # Architecture & credits page
│   ├── student_form/
│   │   ├── form.html           # Practical 1: Registration form
│   │   └── result.html         # Practical 1: Result display
│   ├── hospital/
│   │   ├── appointment.html    # Practical 2: Booking form
│   │   └── confirmation.html   # Practical 2: Confirmation slip
│   ├── students/
│   │   ├── list.html           # Practical 3: Student list & search
│   │   ├── add.html            # Practical 3: Create student
│   │   ├── edit.html           # Practical 3: Update student
│   │   └── details.html        # Practical 3: View student details
│   ├── employees/
│   │   ├── list.html           # Practical 4: Employee list & search
│   │   ├── add.html            # Practical 4: Register employee
│   │   └── edit.html           # Practical 4: Edit employee
│   └── errors/
│       ├── 400.html            # Bad Request / CSRF error
│       ├── 404.html            # Page Not Found
│       └── 500.html            # Server Error
│
├── static/
│   ├── css/
│   │   └── style.css           # Administrative theme & responsive styles
│   └── js/
│       └── main.js             # Sidebar toggle, modals, auto-dismiss alerts
│
└── tests/
    ├── __init__.py
    ├── conftest.py             # Pytest fixtures and temporary database isolation
    └── test_app.py             # Comprehensive automated test suite (36 tests)
```

---

## 7. Installation & Windows Execution

Follow these step-by-step Windows PowerShell commands to clone and execute the application locally:

```powershell
git clone https://github.com/Itzx-kush/Flask-Management-Systems.git

cd Flask-Management-Systems

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

### Accessing the Application

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### Stopping the Development Server

Press `Ctrl+C` in your terminal window to gracefully terminate the Flask server.

---

## 8. Running Automated Tests

The application includes an automated test suite with **36 unit and integration test cases** verifying all four practicals, CSRF protection, database constraints, search filtering, and error handling. Tests execute against an isolated temporary database to keep the development database clean.

Run the tests using `pytest`:

```powershell
venv\Scripts\activate
pytest -v
```

Expected output:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.x, pytest-9.x.x
collected 36 items

tests/test_app.py::test_dashboard_loads PASSED                           [  2%]
tests/test_app.py::test_dashboard_alias_route PASSED                     [  5%]
tests/test_app.py::test_practicals_documentation_loads PASSED            [  8%]
tests/test_app.py::test_about_page_loads PASSED                          [ 11%]
tests/test_app.py::test_404_error_page PASSED                            [ 13%]
tests/test_app.py::test_csrf_protection_mechanism PASSED                 [ 16%]
tests/test_app.py::test_practical_1_student_form_loads PASSED            [ 19%]
tests/test_app.py::test_practical_1_valid_student_information_accepted PASSED [ 22%]
tests/test_app.py::test_practical_1_result_page_displays_submitted_details PASSED [ 25%]
tests/test_app.py::test_practical_1_empty_student_name_rejected PASSED   [ 27%]
tests/test_app.py::test_practical_1_empty_department_rejected PASSED     [ 30%]
tests/test_app.py::test_practical_1_invalid_student_name_characters_rejected PASSED [ 33%]
tests/test_app.py::test_practical_1_unrecognized_department_rejected PASSED [ 36%]
tests/test_app.py::test_practical_2_hospital_appointment_form_loads PASSED [ 38%]
tests/test_app.py::test_practical_2_valid_appointment_accepted_and_confirmed PASSED [ 41%]
tests/test_app.py::test_practical_2_invalid_patient_name_rejected PASSED [ 44%]
tests/test_app.py::test_practical_2_invalid_contact_number_rejected PASSED [ 47%]
tests/test_app.py::test_practical_2_invalid_email_rejected PASSED        [ 50%]
tests/test_app.py::test_practical_2_missing_doctor_rejected PASSED       [ 52%]
tests/test_app.py::test_practical_2_past_appointment_dates_rejected PASSED [ 55%]
tests/test_app.py::test_practical_3_student_database_list_loads PASSED   [ 58%]
tests/test_app.py::test_practical_3_student_creation_works PASSED        [ 61%]
tests/test_app.py::test_practical_3_student_validation_rejects_empty_fields PASSED [ 63%]
tests/test_app.py::test_practical_3_student_records_displayed_and_searched PASSED [ 66%]
tests/test_app.py::test_practical_3_student_details_view PASSED          [ 69%]
tests/test_app.py::test_practical_3_non_existent_student_handled PASSED  [ 72%]
tests/test_app.py::test_practical_3_duplicate_roll_numbers_rejected PASSED [ 75%]
tests/test_app.py::test_practical_3_student_editing_works PASSED         [ 77%]
tests/test_app.py::test_practical_3_student_deletion_works PASSED        [ 80%]
tests/test_app.py::test_practical_4_employee_registration_page_loads PASSED [ 83%]
tests/test_app.py::test_practical_4_employee_creation_and_storage_works PASSED [ 86%]
tests/test_app.py::test_practical_4_employee_validation_rejects_negative_salary PASSED [ 88%]
tests/test_app.py::test_practical_4_employee_records_displayed_and_searched PASSED [ 91%]
tests/test_app.py::test_practical_4_duplicate_employee_id_rejected PASSED [ 94%]
tests/test_app.py::test_practical_4_employee_edit_and_delete PASSED      [ 97%]
tests/test_app.py::test_practical_4_edit_non_existent_employee PASSED    [100%]

============================= 36 passed in 1.82s ==============================
```

---

## 9. UI Screenshots & Previews

| View | Description | Preview |
| :--- | :--- | :--- |
| **Main Dashboard** | Overview statistics, practical module cards, and navigation | *(Dashboard Screenshot)* |
| **Practical 1** | Student form input validation & result display receipt | *(Practical 1 Screenshot)* |
| **Practical 2** | Hospital appointment scheduling with date validation & confirmation | *(Practical 2 Screenshot)* |
| **Practical 3** | Student information CRUD table, add/edit forms, and delete confirmation | *(Practical 3 Screenshot)* |
| **Practical 4** | Employee registration form and SQLite data directory | *(Practical 4 Screenshot)* |
| **Documentation** | Academic lab reports with aims, algorithms, and results | *(Documentation Screenshot)* |

---

## 10. License & Academic Integrity

This project is created for academic practical examination and laboratory demonstration purposes. All code is original and adheres to clean programming practices, parameterized SQL guidelines, and Flask best practices.
