from flask import Blueprint, render_template

practicals_bp = Blueprint('practicals', __name__)


@practicals_bp.route('/practicals')
def practicals():
    """
    Renders the comprehensive Practical Demonstrations documentation page
    covering Aims, Software Requirements, Procedures, Routes, DB Operations,
    Expected Outputs, and Results for all four laboratory practicals.
    """
    return render_template('practicals.html', active_page='practicals')


@practicals_bp.route('/about')
def about():
    """
    Renders the About Project page with system architecture overview,
    developer details, technology stack, and module descriptions.
    """
    return render_template('about.html', active_page='about')
