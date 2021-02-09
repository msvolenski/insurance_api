"""Test User model."""

import pytest
import jwt
from secrets import compare_digest

from application.models.user import User


def test_create_user(test_client):
    """
    GIVEN an user instance
    WHEN the create method is called
    THEN save user to database
    """
    user = User('test@test.com', 'hashed_password')

    count_before = User.query.count()
    created_user = user.create()
    count_after = User.query.count()

    assert count_after == count_before + 1
    assert created_user.id
    assert created_user.email == 'test@test.com'
    assert compare_digest(created_user.password, 'hashed_password')


def test_update_user(test_client):
    """
    GIVEN an user instance
    WHEN the update method is called
    THEN update user in the database
    """
    user = User('test@test.com', 'hashed_password')

    # Prepare test
    created_user = user.create()

    created_info = {
        'id': created_user.id,
        'email': created_user.email,
        'password': created_user.password,
        'first_name': created_user.first_name,
        'address': created_user.address,
        'children': created_user.children,
        'occupation': created_user.occupation
    }

    user.first_name = 'Test'
    user.address = 'Test Blvd'
    user.children = 2
    user.occupation = 'student'

    count_before = User.query.count()
    updated_user = user.update()
    count_after = User.query.count()

    assert count_after == count_before
    assert updated_user.id == created_info['id']
    assert updated_user.email == created_info['email']
    assert compare_digest(updated_user.password, created_info['password'])
    assert updated_user.first_name != created_info['first_name']
    assert updated_user.address != created_info['address']
    assert updated_user.children != created_info['children']
    assert updated_user.occupation != created_info['occupation']


def test_find_by_email(test_client):
    """
    GIVEN an user instance in the database
    WHEN the find_by_email method is called
    THEN return user instance found in the database
    """
    user = User('test@test.com', 'hashed_password')

    # Prepare test
    created_user = user.create()

    found_user = User.find_by_email('test@test.com')

    assert found_user.email == 'test@test.com'
    assert compare_digest(found_user.password, 'hashed_password')


def test_find_by_email_none(test_client):
    """
    GIVEN an user instance in the database
    WHEN the find_by_email method is called
    THEN return user instance found in the database
    """
    user = User.find_by_email('test@test.com')

    assert user is None


def test_encode_auth_token_success(test_client_with_db):
    """
    GIVEN an user id in the database
    WHEN the encode_auth_token method is called
    THEN return JWT token
    """
    user = User.find_by_email('test@test.com')
    token = User.encode_auth_token(user.id)

    assert token is not None


def test_encode_auth_token_exception(test_client, throw_exception_encode_fix):
    """
    GIVEN an user id
    WHEN the encode_auth_token method is called and there's an exception
    THEN raise Exception
    """
    with pytest.raises(Exception):
        User.encode_auth_token(0)


def test_decode_auth_token_success(test_client_with_db):
    """
    GIVEN a valid authentication token
    WHEN the decode_auth_token method is called
    THEN return the user id
    """
    # Prepare test
    user = User.find_by_email('test@test.com')
    token = User.encode_auth_token(user.id)

    payload_sub = User.decode_auth_token(token)

    assert payload_sub == user.id


def test_decode_auth_token_expired_exception(test_client, throw_exception_expired_fix):
    """
    GIVEN an authentication token
    WHEN the decode_auth_token method is called and there's an ExpiredSignatureError exception
    THEN raise Exception
    """
    with pytest.raises(jwt.ExpiredSignatureError):
        User.decode_auth_token('string')


def test_decode_auth_token_invalid_exception(test_client, throw_exception_invalid_token_fix):
    """
    GIVEN an authentication token
    WHEN the decode_auth_token method is called and there's an InvalidTokenError exception
    THEN raise Exception
    """
    with pytest.raises(jwt.InvalidTokenError):
        User.decode_auth_token('string')
