"""Authentication Blueprint."""

from flask import Blueprint, Response, jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash

from application.decorators import validate_input
from application.models.user import User, UserSchema

# Set up a Blueprint
auth_bp = Blueprint('auth_bp', __name__)

# Start validation schemas
user_schema = UserSchema()


@auth_bp.route('/register', methods=('POST',))
@validate_input(schema=user_schema)
def register() -> Response:
    """Register new user.

    :return: JSON response
    """
    # Get data from the request
    data = request.get_json()

    # Check if email is available
    email = data.get('email')
    try:
        if User.find_by_email(email):
            return make_response(jsonify({'message': 'Email already taken.'}), 400)

        # Create user
        User(email, generate_password_hash(data.get('password'))).create()
    except Exception:
        return make_response(jsonify({'message': 'Failed to register user.'}), 500)

    return make_response(jsonify({'message': 'User successfully registered.'}), 200)


@auth_bp.route('/login', methods=('POST',))
@validate_input(schema=user_schema)
def login() -> Response:
    """Log user in.

    :return: JSON response
    """
    # Get data from the request
    data = request.get_json()

    try:
        # Retrieve user for validation
        user = User.find_by_email(data.get('email'))

        # Validate existence of user and correct password hash
        if not user or not check_password_hash(user.password, data.get('password')):
            return make_response(jsonify({'message': 'Invalid email or password.'}), 400)

        # Encode user authentication token
        auth_token = user.encode_auth_token(user.id)
    except Exception:
        return make_response(jsonify({'message': 'Failed to log user in.'}), 500)

    return make_response(jsonify({'access_token': auth_token}), 200)
