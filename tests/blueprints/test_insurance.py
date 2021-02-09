"""Test Insurance APIs."""

import pytest


def test_register_many_insurances_success(test_client):
    """
    GIVEN a list of 2 insurances
    WHEN the insurances API is called
    THEN persist new insurances to database
    """
    data = {
        'insurances': [
            {
                'name': 'Type of Insurance',
                'monthly_price': 50.00
            },
            {
                'name': 'Another Type of Insurance',
                'monthly_price': 99.00
            }
        ]
    }
    response = test_client.post('/insurances', json=data)

    assert response.status_code == 200
    assert response.json['message'] == '2 insurances successfully saved.'

def test_register_1_insurances_success(test_client):
    """
    GIVEN a list of 1 insurance
    WHEN the insurances API is called
    THEN persist new insurance to database
    """
    data = {
        'insurances': [
            {
                'name': 'Type of Insurance',
                'monthly_price': 50.00
            }
        ]
    }
    response = test_client.post('/insurances', json=data)

    assert response.status_code == 200
    assert response.json['message'] == '1 insurance successfully saved.'

def test_register_0_insurances_success(test_client):
    """
    GIVEN a list of 1 insurance already in the database
    WHEN the insurances API is called
    THEN return that no insurances were saved
    """
    data = {
        'insurances': [
            {
                'name': 'name of Insurance',
                'monthly_price': 50.00
            }
        ]
    }
    # Prepare test
    test_client.post('/insurances', json=data)

    response = test_client.post('/insurances', json=data)

    assert response.status_code == 200
    assert response.json['message'] == '0 insurances successfully saved.'

def test_register_insurance_exception(test_client, throw_exception_insurance_fix):
    """
    GIVEN a list of 1 insurance
    WHEN the insurances API is called and there's a server error
    THEN return 500 (Server Error)
    """
    data = {
        'insurances': [
            {
                'name': 'Type of Insurance',
                'monthly_price': 50.00
            }
        ]
    }
    # Prepare test
    test_client.post('/insurances', json=data)

    response = test_client.post('/insurances', json=data)

    assert response.status_code == 500
    assert response.json['message'] == 'Failed to save new insurances.'


def test_recommendation_success(test_client_with_db):
    """
    GIVEN a questionnaire data and an authenticated user
    WHEN the insurances API is called
    THEN return insurance recommendations and update user
    """
    data = {
        'first_name': 'Test',
        'address': 'St. Address, 101',
        'children': 3,
        'occupation': 'employed',
        'email': 'test@test.com'
    }

    # Prepare test
    user_data = {
        'email': 'test@test.com',
        'password': 'password'
    }
    login_response = test_client_with_db.post('/login', json=user_data)

    response = test_client_with_db.post(
        '/recommendation',
        headers={'Authorization': login_response.json['access_token']},
        json=data
    )

    assert response.status_code == 200
    # assert response.json['message'] == '2 insurances successfully saved.'


def test_recommendation_failed_authentication(test_client_with_db):
    """
    GIVEN an authenticated user with and invalid token
    WHEN the insurances API is called
    THEN return 401 (Unauthorized)
    """
    data = {
        'first_name': 'Test',
        'address': 'St. Address, 101',
        'children': 3,
        'occupation': 'employed',
        'email': 'another_test@test.com'
    }

    response = test_client_with_db.post(
        '/recommendation',
        headers={'Authorization': 'invalid_token'},
        json=data
    )

    assert response.status_code == 401
    assert response.json['message'] == ['Invalid token. Please log in again.']


def test_recommendation_unauthorized(test_client):
    """
    GIVEN questionnaire data and non authenticated call
    WHEN the recommendation API is called
    THEN return 401 (Unauthorized)
    """
    data = {
        'first_name': 'Test',
        'address': 'St. Address, 101',
        'children': 3,
        'occupation': 'employed',
        'email': 'test@test.com'
    }
    response = test_client.post('/recommendation', json=data)

    assert response.status_code == 401
    assert response.json['message'] == 'Token missing.'


def test_recommendation_exception(test_client_with_db, throw_exception_recommendation_fix):
    """
    GIVEN a questionnaire data and an authenticated user
    WHEN the insurances API is called and there's a server error
    THEN return 500 (Server Error)
    """
    data = {
        'first_name': 'Test',
        'address': 'St. Address, 101',
        'children': 3,
        'occupation': 'employed',
        'email': 'test@test.com'
    }

    # Prepare test
    user_data = {
        'email': 'test@test.com',
        'password': 'password'
    }
    login_response = test_client_with_db.post('/login', json=user_data)

    response = test_client_with_db.post(
        '/recommendation',
        headers={'Authorization': login_response.json['access_token']},
        json=data
    )

    assert response.status_code == 500
    assert response.json['message'] == 'Failed to get recommendation.'
