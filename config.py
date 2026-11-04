import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'flask-management-systems-dev-secret-key-2026')
    DATABASE = os.path.join(INSTANCE_DIR, 'management.db')
    TESTING = False
    WTF_CSRF_ENABLED = True


class TestConfig(Config):
    TESTING = True
    DATABASE = os.path.join(INSTANCE_DIR, 'test_management.db')
    WTF_CSRF_ENABLED = False
