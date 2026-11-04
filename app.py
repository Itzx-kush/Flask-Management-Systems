import os
import hmac
import secrets
from datetime import datetime
from flask import Flask, session, request, abort, render_template
from config import Config
from database import close_db, init_db
from routes import (
    dashboard_bp,
    student_form_bp,
    hospital_bp,
    students_bp,
    employees_bp,
    practicals_bp
)


def create_app(config_class=Config):
    """
    Application factory for Flask Management Systems.
    Initializes configuration, database, CSRF protection, and blueprints.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register database teardown callback
    app.teardown_appcontext(close_db)

    # Initialize SQLite database schema and seeds
    with app.app_context():
        init_db(app)

    # Context processors and Jinja helpers
    @app.context_processor
    def inject_utilities():
        def csrf_token():
            if '_csrf_token' not in session:
                session['_csrf_token'] = secrets.token_hex(32)
            return session['_csrf_token']

        return {
            'csrf_token': csrf_token,
            'current_year': datetime.now().year,
            'app_version': '1.0.0'
        }

    # CSRF Protection Hook for State-Changing Requests
    @app.before_request
    def check_csrf_protection():
        # Skip CSRF check in automated test mode or when CSRF is disabled
        if app.config.get('TESTING') or not app.config.get('WTF_CSRF_ENABLED', True):
            return

        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            expected_token = session.get('_csrf_token')
            submitted_token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')

            if not expected_token or not submitted_token or not hmac.compare_digest(expected_token, submitted_token):
                abort(400, description="CSRF security validation failed. Please refresh the page and resubmit.")

    # Register Blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(student_form_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(practicals_bp)

    # Custom HTTP Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        message = getattr(error, 'description', 'Bad Request')
        return render_template('errors/400.html', message=message), 400

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    return app


# Create the default application instance
app = create_app()

if __name__ == '__main__':
    # Run the unified application at http://127.0.0.1:5000
    print("================================================================")
    print(" Flask Management Systems — Laboratory Practical Suite")
    print(" Running at: http://127.0.0.1:5000")
    print(" Press Ctrl+C to stop the development server")
    print("================================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
