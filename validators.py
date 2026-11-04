"""
Input validation utilities and regular expressions for all modules.
"""
import re
from datetime import date, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
NAME_REGEX = re.compile(r"^[a-zA-Z\s.'(),-]+$")
PHONE_REGEX = re.compile(r'^\+?[0-9\s-]{10,15}$')
ROLL_REGEX = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
EMP_ID_REGEX = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')

ALLOWED_DEPARTMENTS = [
    'Computer Science & Engineering',
    'Information Technology',
    'Electronics & Communication Engineering',
    'Electrical & Electronics Engineering',
    'Mechanical Engineering',
    'Civil Engineering',
    'Biotechnology',
    'Data Science & AI',
]

SEMESTERS = [
    '1st Semester',
    '2nd Semester',
    '3rd Semester',
    '4th Semester',
    '5th Semester',
    '6th Semester',
    '7th Semester',
    '8th Semester',
]

DOCTORS = [
    {'name': 'Dr. Sarah Jenkins', 'specialization': 'Cardiology', 'id': 'doc_cardio'},
    {'name': 'Dr. Michael Chang', 'specialization': 'Neurology', 'id': 'doc_neuro'},
    {'name': 'Dr. Priya Sharma', 'specialization': 'Pediatrics', 'id': 'doc_pedia'},
    {'name': 'Dr. Robert Davis', 'specialization': 'Orthopedics', 'id': 'doc_ortho'},
    {'name': 'Dr. Elena Rostova', 'specialization': 'Dermatology', 'id': 'doc_derma'},
    {'name': 'Dr. Arvind Mehta', 'specialization': 'General Medicine', 'id': 'doc_genmed'},
    {'name': 'Dr. Susan Taylor', 'specialization': 'Gynecology & Obstetrics', 'id': 'doc_gyn'},
]

EMPLOYEE_DEPARTMENTS = [
    'Engineering',
    'Human Resources',
    'Finance',
    'Marketing & Sales',
    'Operations',
    'Quality Assurance',
    'Research & Development',
]


def is_valid_name(name):
    """Validate that name has letters and spaces, and is between 2 and 60 chars."""
    if not name or not isinstance(name, str):
        return False
    name = name.strip()
    return 2 <= len(name) <= 60 and bool(NAME_REGEX.match(name))


def is_valid_email(email):
    """Validate email address format."""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def is_valid_phone(phone):
    """Validate phone number containing 10-15 digits."""
    if not phone or not isinstance(phone, str):
        return False
    clean = re.sub(r'[\s-]', '', phone.strip())
    # Strip optional leading '+'
    if clean.startswith('+'):
        clean = clean[1:]
    return clean.isdigit() and 10 <= len(clean) <= 15


def is_valid_date(date_str, allow_past=True):
    """
    Validate date format (YYYY-MM-DD) and optionally check that date is not in the past.
    Returns (is_valid, parsed_date, error_message).
    """
    if not date_str or not isinstance(date_str, str):
        return False, None, "Date is required."
    try:
        parsed = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        return False, None, "Invalid date format. Expected YYYY-MM-DD."

    if not allow_past and parsed < date.today():
        return False, parsed, "Appointment date cannot be in the past. Please select today or a future date."

    return True, parsed, None
