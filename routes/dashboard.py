from flask import Blueprint, render_template
from database import query_db

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    """
    Renders the unified main dashboard with quick statistics,
    practical module cards, and administrative shortcuts.
    """
    # Fetch current counts from SQLite tables
    try:
        student_count_row = query_db("SELECT COUNT(*) AS total FROM students", one=True)
        student_count = student_count_row['total'] if student_count_row else 0
    except Exception:
        student_count = 0

    try:
        employee_count_row = query_db("SELECT COUNT(*) AS total FROM employees", one=True)
        employee_count = employee_count_row['total'] if employee_count_row else 0
    except Exception:
        employee_count = 0

    return render_template(
        'dashboard.html',
        student_count=student_count,
        employee_count=employee_count,
        active_page='dashboard'
    )
