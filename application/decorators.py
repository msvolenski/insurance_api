"""Validation decorators."""

from functools import wraps

from flask import request, make_response, jsonify
from marshmallow import Schema

from application.models.user import User


def token_required(f):
    """Validate authentication token.

    :param f:
    :return: JSON Response
    """
    @wraps(f)
    def decorator(*args, **kwargs):

        # Check if token is in the request header
        token = request.headers.get('Authorization', None)

        if not token:
            return make_response(jsonify({'message': 'Token missing.'}), 401)

        # Decode authentication token to check validity
        try:
            User.decode_auth_token(token)
        except Exception as e:
            return make_response(jsonify({'message': e.args}), 401)

        return f(*args, **kwargs)

    return decorator


def validate_input(schema: Schema):
    """Validate request inputs with proper schema.

    :param schema: Schema of the expected input to validate.
    :return: JSON Response
    """
    def inner_function(f):

        @wraps(f)
        def decorator(*args, **kwargs):

            # Check if request is valid
            errors = schema.validate(request.json)
            if errors:
                return make_response(jsonify({'message': errors}), 400)

            return f(*args, **kwargs)

        return decorator

    return inner_function
