import pytest
from datetime import date, timedelta
from app import create_app
from database import query_db


# ============================================================================
# Core & Navigation Tests
# ============================================================================

def test_dashboard_loads(client):
    """Verify that the dashboard and unified landing page load with HTTP 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Flask Management Systems' in response.data
    assert b'Practical 1' in response.data
    assert b'Practical 2' in response.data
    assert b'Practical 3' in response.data
    assert b'Practical 4' in response.data


def test_dashboard_alias_route(client):
    """Verify that /dashboard route also renders the dashboard."""
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Unified Academic Dashboard' in response.data


def test_practicals_documentation_loads(client):
    """Verify that the Practical Demonstrations documentation page loads with HTTP 200."""
    response = client.get('/practicals')
    assert response.status_code == 200
    assert b'Practical Demonstrations' in response.data
    assert b'Laboratory Practical 1' in response.data
    assert b'Laboratory Practical 2' in response.data
    assert b'Laboratory Practical 3' in response.data
    assert b'Laboratory Practical 4' in response.data


def test_about_page_loads(client):
    """Verify that the About Project page loads with HTTP 200."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Flask Management Systems' in response.data
    assert b'Kusumakar Rokkam' in response.data


def test_404_error_page(client):
    """Verify that visiting a non-existent URL returns a 404 error page."""
    response = client.get('/non-existent-page-url')
    assert response.status_code == 404
    assert b'Page Not Found' in response.data


def test_csrf_protection_mechanism():
    """Verify that state-changing POST requests require a valid CSRF token in production."""
    class ProdCSRFConfig:
        TESTING = False
        WTF_CSRF_ENABLED = True
        SECRET_KEY = 'prod-csrf-test-key'
        DATABASE = ':memory:'

    app = create_app(ProdCSRFConfig)
    prod_client = app.test_client()

    # 1. POST without token should be blocked with 400 Bad Request
    unprotected = prod_client.post('/student-form/', data={
        'student_name': 'Valid Name',
        'department': 'Computer Science & Engineering'
    })
    assert unprotected.status_code == 400
    assert b'CSRF security validation failed' in unprotected.data

    # 2. Establish session and obtain valid token
    with prod_client:
        prod_client.get('/student-form/')
        from flask import session
        valid_token = session.get('_csrf_token')
        assert valid_token is not None

        # 3. POST with valid token should pass
        protected = prod_client.post('/student-form/', data={
            'csrf_token': valid_token,
            'student_name': 'Kusumakar Test',
            'department': 'Computer Science & Engineering'
        })
        assert protected.status_code == 200
        assert b'Student Details Submitted' in protected.data



# ============================================================================
# Practical 1: Student Management System Using Flask Forms
# ============================================================================

def test_practical_1_student_form_loads(client):
    """P1: Student form loads successfully."""
    response = client.get('/student-form/')
    assert response.status_code == 200
    assert b'Student Registration Form' in response.data
    assert b'student_name' in response.data
    assert b'department' in response.data


def test_practical_1_valid_student_information_accepted(client):
    """P1: Valid student information is accepted and processes POST request."""
    response = client.post('/student-form/', data={
        'student_name': 'Rahul Dravid',
        'department': 'Computer Science & Engineering'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Student Details Submitted' in response.data


def test_practical_1_result_page_displays_submitted_details(client):
    """P1: Student result page displays the submitted details correctly."""
    response = client.post('/student-form/', data={
        'student_name': 'Sneha Reddy',
        'department': 'Information Technology'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Sneha Reddy' in response.data
    assert b'Information Technology' in response.data
    assert b'Validated (Server-side)' in response.data


def test_practical_1_empty_student_name_rejected(client):
    """P1: Empty student name is rejected with an error message."""
    response = client.post('/student-form/', data={
        'student_name': '',
        'department': 'Mechanical Engineering'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Student Name is required and cannot be empty.' in response.data


def test_practical_1_empty_department_rejected(client):
    """P1: Empty department is rejected with an error message."""
    response = client.post('/student-form/', data={
        'student_name': 'Aditya Verma',
        'department': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please select a valid Department.' in response.data


def test_practical_1_invalid_student_name_characters_rejected(client):
    """P1: Name containing invalid symbols or numbers is rejected."""
    response = client.post('/student-form/', data={
        'student_name': 'John123#$$',
        'department': 'Civil Engineering'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Student Name must contain only alphabetical characters' in response.data


def test_practical_1_unrecognized_department_rejected(client):
    """P1: Department not in allowed list is rejected."""
    response = client.post('/student-form/', data={
        'student_name': 'Valid Name',
        'department': 'Non-existent Department'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid department selected.' in response.data


# ============================================================================
# Practical 2: Hospital Appointment System Using Flask
# ============================================================================

def test_practical_2_hospital_appointment_form_loads(client):
    """P2: Hospital appointment booking form loads successfully."""
    response = client.get('/hospital/')
    assert response.status_code == 200
    assert b'Book a Medical Consultation' in response.data
    assert b'patient_name' in response.data
    assert b'doctor_name' in response.data
    assert b'appointment_date' in response.data
    assert b'contact_number' in response.data
    assert b'email' in response.data


def test_practical_2_valid_appointment_accepted_and_confirmed(client):
    """P2: Valid appointment details are accepted and confirmation displays correct details."""
    future_date = (date.today() + timedelta(days=5)).isoformat()
    response = client.post('/hospital/book', data={
        'patient_name': 'Sunita Krishnan',
        'doctor_name': 'Dr. Sarah Jenkins',
        'appointment_date': future_date,
        'contact_number': '9876543210',
        'email': 'sunita.k@example.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Appointment Confirmed' in response.data
    assert b'Sunita Krishnan' in response.data
    assert b'Dr. Sarah Jenkins' in response.data
    assert b'Cardiology' in response.data
    assert b'9876543210' in response.data
    assert b'sunita.k@example.com' in response.data
    assert b'Confirmed' in response.data
    assert b'APT-' in response.data


def test_practical_2_invalid_patient_name_rejected(client):
    """P2: Invalid patient name is rejected."""
    future_date = (date.today() + timedelta(days=2)).isoformat()
    response = client.post('/hospital/book', data={
        'patient_name': 'P123!@#',
        'doctor_name': 'Dr. Michael Chang',
        'appointment_date': future_date,
        'contact_number': '9876543210',
        'email': 'valid@example.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Patient Name must contain valid alphabetic characters' in response.data


def test_practical_2_invalid_contact_number_rejected(client):
    """P2: Invalid contact number is rejected."""
    future_date = (date.today() + timedelta(days=2)).isoformat()
    response = client.post('/hospital/book', data={
        'patient_name': 'Amitabh Roy',
        'doctor_name': 'Dr. Priya Sharma',
        'appointment_date': future_date,
        'contact_number': '123',  # too short
        'email': 'amitabh@example.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please enter a valid 10-15 digit phone number.' in response.data


def test_practical_2_invalid_email_rejected(client):
    """P2: Invalid email format is rejected."""
    future_date = (date.today() + timedelta(days=2)).isoformat()
    response = client.post('/hospital/book', data={
        'patient_name': 'Amitabh Roy',
        'doctor_name': 'Dr. Priya Sharma',
        'appointment_date': future_date,
        'contact_number': '9876543210',
        'email': 'not-an-email'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please provide a valid email address' in response.data


def test_practical_2_missing_doctor_rejected(client):
    """P2: Missing doctor selection is rejected."""
    future_date = (date.today() + timedelta(days=2)).isoformat()
    response = client.post('/hospital/book', data={
        'patient_name': 'Amitabh Roy',
        'doctor_name': '',
        'appointment_date': future_date,
        'contact_number': '9876543210',
        'email': 'amitabh@example.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please select a consulting doctor.' in response.data


def test_practical_2_past_appointment_dates_rejected(client):
    """P2: Past appointment dates are rejected."""
    past_date = (date.today() - timedelta(days=2)).isoformat()
    response = client.post('/hospital/book', data={
        'patient_name': 'Ramesh Kumar',
        'doctor_name': 'Dr. Robert Davis',
        'appointment_date': past_date,
        'contact_number': '9876543210',
        'email': 'ramesh@example.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Appointment date cannot be in the past' in response.data


# ============================================================================
# Practical 3: Student Information Management System (CRUD & SQLite)
# ============================================================================

def test_practical_3_student_database_list_loads(client):
    """P3: Student database list loads successfully."""
    response = client.get('/students/')
    assert response.status_code == 200
    assert b'Student Information Management System' in response.data
    assert b'Add New Student' in response.data


def test_practical_3_student_creation_works(client):
    """P3: Student creation inserts record into SQLite and redirects to list."""
    response = client.post('/students/add', data={
        'student_name': 'Kavya Madhavan',
        'roll_number': '2024CS9999',
        'department': 'Computer Science & Engineering',
        'email': 'kavya.m@example.edu',
        'phone': '9876543211',
        'semester': '4th Semester'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'added successfully' in response.data
    assert b'2024CS9999' in response.data
    assert b'Kavya Madhavan' in response.data


def test_practical_3_student_validation_rejects_empty_fields(client):
    """P3: Creating student with empty fields displays validation errors."""
    response = client.post('/students/add', data={
        'student_name': '',
        'roll_number': '',
        'department': '',
        'email': 'not-an-email',
        'phone': '12',
        'semester': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Student Name is required.' in response.data
    assert b'Roll Number is required.' in response.data
    assert b'Please select a valid Department.' in response.data


def test_practical_3_student_records_displayed_and_searched(client):
    """P3: Student records are displayed and can be searched."""
    response = client.get('/students/?q=2024CS9999')
    assert response.status_code == 200
    assert b'Kavya Madhavan' in response.data
    assert b'2024CS9999' in response.data


def test_practical_3_student_details_view(client):
    """P3: Individual student details view works."""
    with client.application.app_context():
        student = query_db("SELECT id FROM students WHERE roll_number = '2024CS9999'", one=True)
        assert student is not None
        student_id = student['id']

    response = client.get(f'/students/{student_id}')
    assert response.status_code == 200
    assert b'Kavya Madhavan' in response.data
    assert b'2024CS9999' in response.data


def test_practical_3_non_existent_student_handled(client):
    """P3: Non-existent student details redirects with flash message."""
    response = client.get('/students/999999', follow_redirects=True)
    assert response.status_code == 200
    assert b'was not found' in response.data


def test_practical_3_duplicate_roll_numbers_rejected(client):
    """P3: Duplicate student roll numbers are rejected by SQLite validation."""
    response = client.post('/students/add', data={
        'student_name': 'Another Student',
        'roll_number': '2024CS9999',  # Already exists!
        'department': 'Information Technology',
        'email': 'another@example.edu',
        'phone': '9876543212',
        'semester': '2nd Semester'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'already registered' in response.data


def test_practical_3_student_editing_works(client):
    """P3: Student editing updates existing information in SQLite."""
    with client.application.app_context():
        student = query_db("SELECT id FROM students WHERE roll_number = '2024CS9999'", one=True)
        assert student is not None
        student_id = student['id']

    response = client.post(f'/students/edit/{student_id}', data={
        'student_name': 'Kavya M. Nair',
        'roll_number': '2024CS9999',
        'department': 'Computer Science & Engineering',
        'email': 'kavya.nair@example.edu',
        'phone': '9876543211',
        'semester': '6th Semester'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'updated successfully' in response.data
    assert b'Kavya M. Nair' in response.data
    assert b'6th Semester' in response.data


def test_practical_3_student_deletion_works(client):
    """P3: Student deletion removes record from SQLite."""
    with client.application.app_context():
        student = query_db("SELECT id FROM students WHERE roll_number = '2024CS9999'", one=True)
        assert student is not None
        student_id = student['id']

    response = client.post(f'/students/delete/{student_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'successfully deleted' in response.data

    with client.application.app_context():
        deleted = query_db("SELECT id FROM students WHERE id = ?", (student_id,), one=True)
        assert deleted is None


# ============================================================================
# Practical 4: Employee Management System (Database)
# ============================================================================

def test_practical_4_employee_registration_page_loads(client):
    """P4: Employee registration page loads successfully."""
    response = client.get('/employees/add')
    assert response.status_code == 200
    assert b'Employee Registration Form' in response.data
    assert b'employee_id' in response.data
    assert b'salary' in response.data


def test_practical_4_employee_creation_and_storage_works(client):
    """P4: Employee creation works and information is stored in SQLite."""
    response = client.post('/employees/add', data={
        'employee_id': 'EMP-7701',
        'employee_name': 'Harish Kalyan',
        'department': 'Engineering',
        'designation': 'DevOps Lead',
        'email': 'harish.k@enterprise.org',
        'phone': '9812345670',
        'salary': '115000',
        'joining_date': '2023-04-01'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'registered successfully in SQLite' in response.data
    assert b'EMP-7701' in response.data
    assert b'Harish Kalyan' in response.data


def test_practical_4_employee_validation_rejects_negative_salary(client):
    """P4: Negative salary is rejected."""
    response = client.post('/employees/add', data={
        'employee_id': 'EMP-9901',
        'employee_name': 'Invalid Salary Person',
        'department': 'Finance',
        'designation': 'Clerk',
        'email': 'clerk@enterprise.org',
        'phone': '9812345670',
        'salary': '-500',
        'joining_date': '2023-01-01'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Salary must be a positive amount' in response.data


def test_practical_4_employee_records_displayed_and_searched(client):
    """P4: Employee records are displayed in table and searchable."""
    response = client.get('/employees/?q=EMP-7701')
    assert response.status_code == 200
    assert b'Harish Kalyan' in response.data
    assert b'EMP-7701' in response.data
    assert b'DevOps Lead' in response.data
    assert b'$115,000.00' in response.data


def test_practical_4_duplicate_employee_id_rejected(client):
    """P4: Duplicate employee IDs are rejected by SQLite validation."""
    response = client.post('/employees/add', data={
        'employee_id': 'EMP-7701',  # Duplicate!
        'employee_name': 'Duplicate User',
        'department': 'Finance',
        'designation': 'Financial Analyst',
        'email': 'duplicate@enterprise.org',
        'phone': '9812345679',
        'salary': '60000',
        'joining_date': '2023-05-01'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'already assigned' in response.data


def test_practical_4_employee_edit_and_delete(client):
    """P4: Employee editing and deletion operations work."""
    with client.application.app_context():
        emp = query_db("SELECT id FROM employees WHERE employee_id = 'EMP-7701'", one=True)
        assert emp is not None
        emp_id = emp['id']

    # Update employee
    edit_response = client.post(f'/employees/edit/{emp_id}', data={
        'employee_id': 'EMP-7701',
        'employee_name': 'Harish Kalyan (Senior Lead)',
        'department': 'Engineering',
        'designation': 'Principal DevOps Architect',
        'email': 'harish.kalyan@enterprise.org',
        'phone': '9812345670',
        'salary': '135000',
        'joining_date': '2023-04-01'
    }, follow_redirects=True)

    assert edit_response.status_code == 200
    assert b'updated successfully' in edit_response.data
    assert b'Principal DevOps Architect' in edit_response.data

    # Delete employee
    del_response = client.post(f'/employees/delete/{emp_id}', follow_redirects=True)
    assert del_response.status_code == 200
    assert b'was deleted successfully' in del_response.data

    with client.application.app_context():
        deleted = query_db("SELECT id FROM employees WHERE id = ?", (emp_id,), one=True)
        assert deleted is None


def test_practical_4_edit_non_existent_employee(client):
    """P4: Non-existent employee returns warning and redirects."""
    response = client.get('/employees/edit/999999', follow_redirects=True)
    assert response.status_code == 200
    assert b'was not found' in response.data
