import pytest
from backend import create_app
from backend.config import TestingConfig
from backend.models import db


@pytest.fixture
def app():
    """Create application configured for testing with an in-memory SQLite database."""
    application = create_app(config_class=TestingConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the application."""
    return app.test_client()
