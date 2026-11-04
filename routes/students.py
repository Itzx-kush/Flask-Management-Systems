from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import query_db, execute_db
from validators import (
    ALLOWED_DEPARTMENTS,
    SEMESTERS,
    is_valid_name,
    is_valid_email,
    is_valid_phone,
    ROLL_REGEX
)

students_bp = Blueprint('students', __name__, url_prefix='/students')


@students_bp.route('/', methods=['GET'])
def list_students():
    """
    READ (List & Search):
    Retrieves students from SQLite database with optional search filtering by name or roll number.
    """
    search_query = request.args.get('q', '').strip()

    if search_query:
        param = f"%{search_query}%"
        students = query_db(
            """
            SELECT * FROM students
            WHERE student_name LIKE ? OR roll_number LIKE ? OR department LIKE ?
            ORDER BY id DESC
            """,
            (param, param, param)
        )
    else:
        students = query_db("SELECT * FROM students ORDER BY id DESC")

    return render_template(
        'students/list.html',
        students=students,
        search_query=search_query,
        active_page='students'
    )


@students_bp.route('/<int:id>', methods=['GET'])
def details(id):
    """
    READ (Details):
    Displays individual student record details.
    """
    student = query_db("SELECT * FROM students WHERE id = ?", (id,), one=True)
    if student is None:
        flash(f"Student with ID #{id} was not found.", "warning")
        return redirect(url_for('students.list_students'))

    return render_template(
        'students/details.html',
        student=student,
        active_page='students'
    )


@students_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    """
    CREATE:
    Validates input, checks for duplicate roll numbers, and inserts a new student record into SQLite.
    """
    errors = {}
    form_data = {
        'student_name': '',
        'roll_number': '',
        'department': '',
        'email': '',
        'phone': '',
        'semester': ''
    }

    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        roll_number = request.form.get('roll_number', '').strip().upper()
        department = request.form.get('department', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        semester = request.form.get('semester', '').strip()

        form_data = {
            'student_name': student_name,
            'roll_number': roll_number,
            'department': department,
            'email': email,
            'phone': phone,
            'semester': semester
        }

        # Validate student name
        if not student_name:
            errors['student_name'] = 'Student Name is required.'
        elif not is_valid_name(student_name):
            errors['student_name'] = 'Student Name must contain valid characters (2-60 letters).'

        # Validate roll number format
        if not roll_number:
            errors['roll_number'] = 'Roll Number is required.'
        elif not ROLL_REGEX.match(roll_number):
            errors['roll_number'] = 'Roll Number must be alphanumeric (3-20 characters, e.g., 2024CS0101).'
        else:
            # Check unique constraint in SQLite
            existing = query_db("SELECT id FROM students WHERE roll_number = ?", (roll_number,), one=True)
            if existing:
                errors['roll_number'] = f'Roll Number "{roll_number}" is already registered.'

        # Validate department
        if not department or department not in ALLOWED_DEPARTMENTS:
            errors['department'] = 'Please select a valid Department.'

        # Validate email
        if not email:
            errors['email'] = 'Email is required.'
        elif not is_valid_email(email):
            errors['email'] = 'Please provide a valid email address.'

        # Validate phone
        if not phone:
            errors['phone'] = 'Phone Number is required.'
        elif not is_valid_phone(phone):
            errors['phone'] = 'Please enter a valid 10-15 digit phone number.'

        # Validate semester
        if not semester or semester not in SEMESTERS:
            errors['semester'] = 'Please select a valid Semester.'

        if errors:
            flash('Please correct the errors in the student form.', 'danger')
            return render_template(
                'students/add.html',
                errors=errors,
                form_data=form_data,
                departments=ALLOWED_DEPARTMENTS,
                semesters=SEMESTERS,
                active_page='students'
            )

        # Insert student record
        execute_db(
            """
            INSERT INTO students (student_name, roll_number, department, email, phone, semester)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (student_name, roll_number, department, email, phone, semester)
        )

        flash(f'Student "{student_name}" (Roll: {roll_number}) added successfully!', 'success')
        return redirect(url_for('students.list_students'))

    return render_template(
        'students/add.html',
        errors=errors,
        form_data=form_data,
        departments=ALLOWED_DEPARTMENTS,
        semesters=SEMESTERS,
        active_page='students'
    )


@students_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    """
    UPDATE:
    Loads existing student record into form, validates updates, prevents duplicate roll numbers,
    and updates the database.
    """
    student = query_db("SELECT * FROM students WHERE id = ?", (id,), one=True)
    if student is None:
        flash(f"Student with ID #{id} was not found.", "warning")
        return redirect(url_for('students.list_students'))

    errors = {}
    form_data = dict(student)

    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        roll_number = request.form.get('roll_number', '').strip().upper()
        department = request.form.get('department', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        semester = request.form.get('semester', '').strip()

        form_data = {
            'id': id,
            'student_name': student_name,
            'roll_number': roll_number,
            'department': department,
            'email': email,
            'phone': phone,
            'semester': semester,
            'created_at': student['created_at']
        }

        # Validations
        if not student_name:
            errors['student_name'] = 'Student Name is required.'
        elif not is_valid_name(student_name):
            errors['student_name'] = 'Student Name must contain valid characters (2-60 letters).'

        if not roll_number:
            errors['roll_number'] = 'Roll Number is required.'
        elif not ROLL_REGEX.match(roll_number):
            errors['roll_number'] = 'Roll Number must be alphanumeric (3-20 characters).'
        else:
            # Check unique constraint against OTHER students
            existing = query_db("SELECT id FROM students WHERE roll_number = ? AND id != ?", (roll_number, id), one=True)
            if existing:
                errors['roll_number'] = f'Roll Number "{roll_number}" is already used by another student.'

        if not department or department not in ALLOWED_DEPARTMENTS:
            errors['department'] = 'Please select a valid Department.'

        if not email or not is_valid_email(email):
            errors['email'] = 'Please provide a valid email address.'

        if not phone or not is_valid_phone(phone):
            errors['phone'] = 'Please enter a valid 10-15 digit phone number.'

        if not semester or semester not in SEMESTERS:
            errors['semester'] = 'Please select a valid Semester.'

        if errors:
            flash('Please correct the errors in the update form.', 'danger')
            return render_template(
                'students/edit.html',
                student=student,
                errors=errors,
                form_data=form_data,
                departments=ALLOWED_DEPARTMENTS,
                semesters=SEMESTERS,
                active_page='students'
            )

        # Update record
        execute_db(
            """
            UPDATE students
            SET student_name = ?, roll_number = ?, department = ?, email = ?, phone = ?, semester = ?
            WHERE id = ?
            """,
            (student_name, roll_number, department, email, phone, semester, id)
        )

        flash(f'Student "{student_name}" updated successfully!', 'success')
        return redirect(url_for('students.details', id=id))

    return render_template(
        'students/edit.html',
        student=student,
        errors=errors,
        form_data=form_data,
        departments=ALLOWED_DEPARTMENTS,
        semesters=SEMESTERS,
        active_page='students'
    )


@students_bp.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    """
    DELETE:
    Deletes the student record from SQLite after user confirmation.
    """
    student = query_db("SELECT * FROM students WHERE id = ?", (id,), one=True)
    if student is None:
        flash(f"Student with ID #{id} does not exist.", "warning")
        return redirect(url_for('students.list_students'))

    execute_db("DELETE FROM students WHERE id = ?", (id,))
    flash(f'Student "{student["student_name"]}" (Roll: {student["roll_number"]}) was successfully deleted.', 'info')
    return redirect(url_for('students.list_students'))
