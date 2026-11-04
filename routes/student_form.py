from datetime import datetime
from flask import Blueprint, render_template, request, flash
from validators import is_valid_name, ALLOWED_DEPARTMENTS

student_form_bp = Blueprint('student_form', __name__, url_prefix='/student-form')


@student_form_bp.route('/', methods=['GET', 'POST'])
def form():
    """
    Practical 1: Basic Flask Form Handling & Server-side Validation.
    Accepts student name and department, validates inputs without database persistence,
    and displays submitted details on a result page.
    """
    errors = {}
    form_data = {
        'student_name': '',
        'department': ''
    }

    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        department = request.form.get('department', '').strip()

        form_data['student_name'] = student_name
        form_data['department'] = department

        # Validation 1: Student Name not empty
        if not student_name:
            errors['student_name'] = 'Student Name is required and cannot be empty.'
        # Validation 2: Student Name valid characters and length
        elif not is_valid_name(student_name):
            errors['student_name'] = 'Student Name must contain only alphabetical characters, spaces, dots or hyphens (2-60 characters).'

        # Validation 3: Department not empty
        if not department:
            errors['department'] = 'Please select a valid Department.'
        # Validation 4: Department must be within the allowed list
        elif department not in ALLOWED_DEPARTMENTS:
            errors['department'] = 'Invalid department selected.'

        # If errors exist, render the form back with errors and feedback
        if errors:
            flash('Please correct the highlighted errors before proceeding.', 'danger')
            return render_template(
                'student_form/form.html',
                errors=errors,
                form_data=form_data,
                departments=ALLOWED_DEPARTMENTS,
                active_page='student_form'
            )

        # Successful submission: Render result page
        flash(f'Student details for "{student_name}" submitted and validated successfully!', 'success')
        submission_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        return render_template(
            'student_form/result.html',
            student_name=student_name,
            department=department,
            submission_time=submission_time,
            active_page='student_form'
        )

    # GET request: Render blank registration form
    return render_template(
        'student_form/form.html',
        errors=errors,
        form_data=form_data,
        departments=ALLOWED_DEPARTMENTS,
        active_page='student_form'
    )
