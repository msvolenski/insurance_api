"""Pytest fixtures for testing."""

import pytest

import jwt
from werkzeug.security import generate_password_hash

from application import db, create_app
from application.models.insurance import Insurance
from application.models.user import User


@pytest.fixture(scope='function')
def test_client():
    flask_app = create_app('config.Test')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope='function')
def test_client_with_db():
    flask_app = create_app('config.Test')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            db.create_all()

            # Insert user data
            user = User('test@test.com', generate_password_hash('password'))
            db.session.add(user)

            # Insert insurance data
            insurances = [
                Insurance('Private Health Insurance', 300.00),
                Insurance('Household Contents Insurance', 10.00),
                Insurance('Public Health Insurance', 200.00),
                Insurance('Expat Health Insurance', 85.00),
                Insurance('Legal Insurance', 25.00),
                Insurance('Life Insurance', 20.00)
            ]
            db.session.bulk_save_objects(insurances)

            # Commit the changes for the users
            db.session.commit()

            yield testing_client
            db.drop_all()


def mock_exception(*args, **kwargs):
    raise Exception


@pytest.fixture
def throw_exception_register_fix(monkeypatch):
    monkeypatch.setattr(User, 'create', mock_exception)


@pytest.fixture
def throw_exception_login_fix(monkeypatch):
    monkeypatch.setattr(User, 'encode_auth_token', mock_exception)


@pytest.fixture
def throw_exception_insurance_fix(monkeypatch):
    monkeypatch.setattr(Insurance, 'create', mock_exception)


@pytest.fixture
def throw_exception_recommendation_fix(monkeypatch):
    monkeypatch.setattr(User, 'update', mock_exception)


@pytest.fixture
def throw_exception_encode_fix(monkeypatch):
    monkeypatch.setattr(jwt, 'encode', mock_exception)


def mock_expired_exception(*args, **kwargs):
    raise jwt.ExpiredSignatureError


@pytest.fixture
def throw_exception_expired_fix(monkeypatch):
    monkeypatch.setattr(jwt, 'decode', mock_expired_exception)


def mock_invalid_token_exception(*args, **kwargs):
    raise jwt.InvalidTokenError


@pytest.fixture
def throw_exception_invalid_token_fix(monkeypatch):
    monkeypatch.setattr(jwt, 'decode', mock_invalid_token_exception)
