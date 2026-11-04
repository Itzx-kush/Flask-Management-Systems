"""
Routes package initialization.
Exports all blueprints for unified registration in app.py.
"""
from routes.dashboard import dashboard_bp
from routes.student_form import student_form_bp
from routes.hospital import hospital_bp
from routes.students import students_bp
from routes.employees import employees_bp
from routes.practicals import practicals_bp

__all__ = [
    'dashboard_bp',
    'student_form_bp',
    'hospital_bp',
    'students_bp',
    'employees_bp',
    'practicals_bp',
]
