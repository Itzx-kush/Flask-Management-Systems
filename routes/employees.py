from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import query_db, execute_db
from validators import (
    EMPLOYEE_DEPARTMENTS,
    is_valid_name,
    is_valid_email,
    is_valid_phone,
    EMP_ID_REGEX
)

employees_bp = Blueprint('employees', __name__, url_prefix='/employees')


@employees_bp.route('/', methods=['GET'])
def list_employees():
    """
    Practical 4: Retrieves and displays stored employee records from SQLite database.
    Supports optional search filtering by employee name or employee ID.
    """
    search_query = request.args.get('q', '').strip()

    if search_query:
        param = f"%{search_query}%"
        employees = query_db(
            """
            SELECT * FROM employees
            WHERE employee_name LIKE ? OR employee_id LIKE ? OR department LIKE ? OR designation LIKE ?
            ORDER BY id DESC
            """,
            (param, param, param, param)
        )
    else:
        employees = query_db("SELECT * FROM employees ORDER BY id DESC")

    return render_template(
        'employees/list.html',
        employees=employees,
        search_query=search_query,
        active_page='employees'
    )


@employees_bp.route('/add', methods=['GET', 'POST'])
def add_employee():
    """
    Practical 4: Displays employee registration form, validates input,
    ensures unique employee ID, stores employee information in SQLite,
    and displays success notification.
    """
    errors = {}
    form_data = {
        'employee_id': '',
        'employee_name': '',
        'department': '',
        'designation': '',
        'email': '',
        'phone': '',
        'salary': '',
        'joining_date': ''
    }

    if request.method == 'POST':
        employee_id = request.form.get('employee_id', '').strip().upper()
        employee_name = request.form.get('employee_name', '').strip()
        department = request.form.get('department', '').strip()
        designation = request.form.get('designation', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        salary_str = request.form.get('salary', '').strip()
        joining_date = request.form.get('joining_date', '').strip()

        form_data = {
            'employee_id': employee_id,
            'employee_name': employee_name,
            'department': department,
            'designation': designation,
            'email': email,
            'phone': phone,
            'salary': salary_str,
            'joining_date': joining_date
        }

        # 1. Validate Employee ID
        if not employee_id:
            errors['employee_id'] = 'Employee ID is required.'
        elif not EMP_ID_REGEX.match(employee_id):
            errors['employee_id'] = 'Employee ID must be alphanumeric (e.g., EMP-1005 or E102).'
        else:
            existing = query_db("SELECT id FROM employees WHERE employee_id = ?", (employee_id,), one=True)
            if existing:
                errors['employee_id'] = f'Employee ID "{employee_id}" is already assigned.'

        # 2. Validate Employee Name
        if not employee_name:
            errors['employee_name'] = 'Employee Name is required.'
        elif not is_valid_name(employee_name):
            errors['employee_name'] = 'Employee Name must contain valid characters (2-60 letters).'

        # 3. Validate Department
        if not department:
            errors['department'] = 'Please select or enter a Department.'

        # 4. Validate Designation
        if not designation:
            errors['designation'] = 'Designation is required.'

        # 5. Validate Email
        if not email:
            errors['email'] = 'Email Address is required.'
        elif not is_valid_email(email):
            errors['email'] = 'Please provide a valid corporate email address.'

        # 6. Validate Phone
        if not phone:
            errors['phone'] = 'Contact Phone is required.'
        elif not is_valid_phone(phone):
            errors['phone'] = 'Please enter a valid 10-15 digit phone number.'

        # 7. Validate Salary
        salary = 0.0
        if not salary_str:
            errors['salary'] = 'Salary is required.'
        else:
            try:
                salary = float(salary_str)
                if salary <= 0:
                    errors['salary'] = 'Salary must be a positive amount greater than zero.'
            except ValueError:
                errors['salary'] = 'Salary must be a valid numeric amount.'

        # 8. Validate Joining Date
        if not joining_date:
            errors['joining_date'] = 'Joining Date is required.'
        else:
            try:
                datetime.strptime(joining_date, "%Y-%m-%d")
            except ValueError:
                errors['joining_date'] = 'Invalid date format (expected YYYY-MM-DD).'

        if errors:
            flash('Please correct the errors in the employee form.', 'danger')
            return render_template(
                'employees/add.html',
                errors=errors,
                form_data=form_data,
                departments=EMPLOYEE_DEPARTMENTS,
                active_page='employees'
            )

        try:
            execute_db(
                """
                INSERT INTO employees (
                    employee_id, employee_name, department, designation, email, phone, salary, joining_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (employee_id, employee_name, department, designation, email, phone, salary, joining_date)
            )
            flash(f'Employee "{employee_name}" ({employee_id}) registered successfully in SQLite database!', 'success')
            return redirect(url_for('employees.list_employees'))
        except Exception as e:
            flash(f'Database error while saving employee: {str(e)}', 'danger')
            return render_template(
                'employees/add.html',
                errors=errors,
                form_data=form_data,
                departments=EMPLOYEE_DEPARTMENTS,
                active_page='employees'
            )

    return render_template(
        'employees/add.html',
        errors=errors,
        form_data=form_data,
        departments=EMPLOYEE_DEPARTMENTS,
        active_page='employees'
    )


@employees_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    """
    Bonus Feature: Edit existing employee details while preserving unique employee ID check.
    """
    employee = query_db("SELECT * FROM employees WHERE id = ?", (id,), one=True)
    if employee is None:
        flash(f"Employee with ID #{id} was not found.", "warning")
        return redirect(url_for('employees.list_employees'))

    errors = {}
    form_data = dict(employee)

    if request.method == 'POST':
        employee_id = request.form.get('employee_id', '').strip().upper()
        employee_name = request.form.get('employee_name', '').strip()
        department = request.form.get('department', '').strip()
        designation = request.form.get('designation', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        salary_str = request.form.get('salary', '').strip()
        joining_date = request.form.get('joining_date', '').strip()

        form_data = {
            'id': id,
            'employee_id': employee_id,
            'employee_name': employee_name,
            'department': department,
            'designation': designation,
            'email': email,
            'phone': phone,
            'salary': salary_str,
            'joining_date': joining_date,
            'created_at': employee['created_at']
        }

        # Validations
        if not employee_id:
            errors['employee_id'] = 'Employee ID is required.'
        elif not EMP_ID_REGEX.match(employee_id):
            errors['employee_id'] = 'Employee ID must be alphanumeric.'
        else:
            existing = query_db("SELECT id FROM employees WHERE employee_id = ? AND id != ?", (employee_id, id), one=True)
            if existing:
                errors['employee_id'] = f'Employee ID "{employee_id}" is assigned to another employee.'

        if not employee_name or not is_valid_name(employee_name):
            errors['employee_name'] = 'Employee Name must contain valid characters.'

        if not department:
            errors['department'] = 'Department is required.'

        if not designation:
            errors['designation'] = 'Designation is required.'

        if not email or not is_valid_email(email):
            errors['email'] = 'Valid email is required.'

        if not phone or not is_valid_phone(phone):
            errors['phone'] = 'Valid phone is required.'

        salary = 0.0
        try:
            salary = float(salary_str)
            if salary <= 0:
                errors['salary'] = 'Salary must be greater than zero.'
        except ValueError:
            errors['salary'] = 'Salary must be a valid number.'

        if not joining_date:
            errors['joining_date'] = 'Joining date is required.'

        if errors:
            flash('Please correct the errors in the update form.', 'danger')
            return render_template(
                'employees/edit.html',
                employee=employee,
                errors=errors,
                form_data=form_data,
                departments=EMPLOYEE_DEPARTMENTS,
                active_page='employees'
            )

        try:
            execute_db(
                """
                UPDATE employees
                SET employee_id = ?, employee_name = ?, department = ?, designation = ?,
                    email = ?, phone = ?, salary = ?, joining_date = ?
                WHERE id = ?
                """,
                (employee_id, employee_name, department, designation, email, phone, salary, joining_date, id)
            )
            flash(f'Employee record for "{employee_name}" updated successfully!', 'success')
            return redirect(url_for('employees.list_employees'))
        except Exception as e:
            flash(f'Database error: {str(e)}', 'danger')
            return render_template(
                'employees/edit.html',
                employee=employee,
                errors=errors,
                form_data=form_data,
                departments=EMPLOYEE_DEPARTMENTS,
                active_page='employees'
            )

    return render_template(
        'employees/edit.html',
        employee=employee,
        errors=errors,
        form_data=form_data,
        departments=EMPLOYEE_DEPARTMENTS,
        active_page='employees'
    )


@employees_bp.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    """
    Bonus Feature: Delete employee record from SQLite with user confirmation.
    """
    employee = query_db("SELECT * FROM employees WHERE id = ?", (id,), one=True)
    if employee is None:
        flash(f"Employee with ID #{id} was not found.", "warning")
        return redirect(url_for('employees.list_employees'))

    execute_db("DELETE FROM employees WHERE id = ?", (id,))
    flash(f'Employee "{employee["employee_name"]}" ({employee["employee_id"]}) was deleted successfully.', 'info')
    return redirect(url_for('employees.list_employees'))
