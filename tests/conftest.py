import os
import tempfile
import pytest
from app import create_app
from database import init_db


@pytest.fixture(scope='session')
def temp_db_path():
    """Generates a temporary database path that does not affect development data."""
    fd, path = tempfile.mkstemp(suffix='.db', prefix='flask_test_')
    os.close(fd)
    yield path
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


@pytest.fixture
def app(temp_db_path):
    """Creates a configured test application instance using the temporary database."""
    class TestingConfig:
        TESTING = True
        SECRET_KEY = 'test-secret-key-12345'
        DATABASE = temp_db_path
        WTF_CSRF_ENABLED = False

    test_app = create_app(TestingConfig)

    # Initialize tables
    with test_app.app_context():
        init_db(test_app, db_path=temp_db_path)

    yield test_app


@pytest.fixture
def client(app):
    """Provides a test client for simulating HTTP requests."""
    return app.test_client()
