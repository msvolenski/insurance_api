"""Test Authentication APIs."""

import pytest


def test_register_user_success(test_client):
    """
    GIVEN an unregistered user data
    WHEN the register API is called
    THEN persist new user to database
    """
    data = {
        'email': 'test@test.com',
        'password': 'password'
    }
    response = test_client.post('/register', json=data)

    assert response.status_code == 200
    assert response.json['message'] == 'User successfully registered.'


def test_register_user_invalid_data(test_client):
    """
    GIVEN invalid user data
    WHEN the register API is called
    THEN return invalid data error
    """
    data = {
        'email': 'test_test.com',
        'password': 'pass'
    }
    response = test_client.post('/register', json=data)

    assert response.status_code == 400
    assert response.json['message']['email'][0] == 'Not a valid email address.'
    assert response.json['message']['password'][0] == 'Length must be between 8 and 30.'


def test_register_duplicate_user(test_client):
    """
    GIVEN a registered user data
    WHEN the register API is called
    THEN return that user already exists
    """
    data = {
        'email': 'test@test.com',
        'password': 'password'
    }
    # Register user
    test_client.post('/register', json=data)

    data = {
        'email': 'test@test.com',
        'password': 'another_password'
    }

    # Try to register user with the same email
    response = test_client.post('/register', json=data)

    assert response.status_code == 400
    assert response.json['message'] == 'Email already taken.'


def test_register_user_exception(test_client, throw_exception_register_fix):
    """
    GIVEN an unregistered user data
    WHEN the register API is called and there's a server exception
    THEN return 500 (Server Error)
    """
    data = {
        'email': 'test@test.com',
        'password': 'password'
    }
    response = test_client.post('/register', json=data)

    assert response.status_code == 500
    assert response.json['message'] == 'Failed to register user.'


def test_login_success(test_client):
    """
    GIVEN a registered user data
    WHEN the login API is called
    THEN the user is logged in and a token is issued
    """
    data = {
        'email': 'test@test.com',
        'password': 'password'
    }
    # Prepare test
    test_client.post('/register', json=data)

    response = test_client.post('/login', json=data)

    assert response.status_code == 200
    assert response.json['access_token']


def test_login_wrong_data(test_client):
    """
    GIVEN a valid unregistered user data
    WHEN the login API is called
    THEN return invalid data error
    """
    data = {
        'email': 'test@test.com',
        'password': 'password'
    }
    response = test_client.post('/login', json=data)

    assert response.status_code == 400
    assert response.json['message'] == 'Invalid email or password.'


def test_login_invalid_data(test_client):
    """
    GIVEN invalid user data
    WHEN the register API is called
    THEN return invalid data error
    """
    data = {
        'email': 'test_test.com',
        'password': 'pass'
    }
    response = test_client.post('/login', json=data)

    assert response.status_code == 400
    assert response.json['message']['email'][0] == 'Not a valid email address.'
    assert response.json['message']['password'][0] == 'Length must be between 8 and 30.'


def test_login_exception(test_client, throw_exception_login_fix):
    """
    GIVEN a register user data
    WHEN the login API is called and there's a server exception
    THEN return 500 (Server Error)
    """
    data = {
        'email': 'test@test.com',
        'password': 'password'
    }
    # Prepare test
    test_client.post('/register', json=data)

    response = test_client.post('/login', json=data)

    assert response.status_code == 500
    assert response.json['message'] == 'Failed to log user in.'
