import random
import string
from datetime import date
from flask import Blueprint, render_template, request, flash
from validators import (
    DOCTORS,
    is_valid_name,
    is_valid_email,
    is_valid_phone,
    is_valid_date
)

hospital_bp = Blueprint('hospital', __name__, url_prefix='/hospital')


def generate_appointment_id():
    """Generates a professional academic appointment tracking reference."""
    today_str = date.today().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"APT-{today_str}-{random_suffix}"


@hospital_bp.route('/', methods=['GET'])
def index():
    """Renders the hospital appointment booking form."""
    min_date = date.today().isoformat()
    return render_template(
        'hospital/appointment.html',
        doctors=DOCTORS,
        min_date=min_date,
        form_data={},
        errors={},
        active_page='hospital'
    )


@hospital_bp.route('/book', methods=['POST'])
def book_appointment():
    """
    Practical 2: Processes appointment booking form with multi-field validation,
    ensures appointment date is not in the past, and displays confirmation page.
    """
    patient_name = request.form.get('patient_name', '').strip()
    doctor_name = request.form.get('doctor_name', '').strip()
    appointment_date_str = request.form.get('appointment_date', '').strip()
    contact_number = request.form.get('contact_number', '').strip()
    email = request.form.get('email', '').strip()

    form_data = {
        'patient_name': patient_name,
        'doctor_name': doctor_name,
        'appointment_date': appointment_date_str,
        'contact_number': contact_number,
        'email': email
    }
    errors = {}

    # 1. Validate Patient Name
    if not patient_name:
        errors['patient_name'] = 'Patient Name is required.'
    elif not is_valid_name(patient_name):
        errors['patient_name'] = 'Patient Name must contain valid alphabetic characters (2-60 chars).'

    # 2. Validate Doctor Selection
    valid_doctor_names = [d['name'] for d in DOCTORS]
    if not doctor_name:
        errors['doctor_name'] = 'Please select a consulting doctor.'
    elif doctor_name not in valid_doctor_names:
        errors['doctor_name'] = 'Selected doctor is not recognized in our hospital directory.'

    # 3. Validate Appointment Date (prevent booking in past)
    date_valid, parsed_date, date_err = is_valid_date(appointment_date_str, allow_past=False)
    if not date_valid:
        errors['appointment_date'] = date_err

    # 4. Validate Contact Number
    if not contact_number:
        errors['contact_number'] = 'Contact Number is required.'
    elif not is_valid_phone(contact_number):
        errors['contact_number'] = 'Please enter a valid 10-15 digit phone number.'

    # 5. Validate Email Address
    if not email:
        errors['email'] = 'Email Address is required.'
    elif not is_valid_email(email):
        errors['email'] = 'Please provide a valid email address (e.g., patient@example.com).'

    # If any validation errors exist, re-render the form with error highlights
    if errors:
        flash('Appointment request could not be processed due to validation errors.', 'danger')
        min_date = date.today().isoformat()
        return render_template(
            'hospital/appointment.html',
            doctors=DOCTORS,
            min_date=min_date,
            form_data=form_data,
            errors=errors,
            active_page='hospital'
        )

    # Find doctor specialization
    doctor_info = next((d for d in DOCTORS if d['name'] == doctor_name), None)
    specialization = doctor_info['specialization'] if doctor_info else "General Medicine"

    appointment_id = generate_appointment_id()
    formatted_date = parsed_date.strftime("%A, %B %d, %Y")

    flash('Appointment booked successfully! Details are confirmed below.', 'success')
    return render_template(
        'hospital/confirmation.html',
        appointment_id=appointment_id,
        patient_name=patient_name,
        doctor_name=doctor_name,
        specialization=specialization,
        appointment_date=formatted_date,
        contact_number=contact_number,
        email=email,
        status="Confirmed",
        active_page='hospital'
    )
