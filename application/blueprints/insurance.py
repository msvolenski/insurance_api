"""Insurance Blueprint."""

from typing import Optional

from flask import Blueprint, Response, jsonify, make_response, request

from application.decorators import token_required, validate_input
from application.models.insurance import (
    Insurance, InsuranceListSchema, InsuranceSchema, QuestionnaireSchema
)
from application.models.user import User

# Set up a Blueprint
insurance_bp = Blueprint('insurance_bp', __name__)

# Start validation schemas
questionnaire_schema = QuestionnaireSchema()
insurance_list_schema = InsuranceListSchema()
insurance_schema = InsuranceSchema()


@insurance_bp.route('/recommendation', methods=('POST',))
@token_required
@validate_input(schema=questionnaire_schema)
def recommendation() -> Response:
    """Get insurance recommendation.

    :return: JSON response
    """
    # Get data from the request
    data = request.get_json()

    try:
        # Check if email is registered
        user: Optional[User] = User.find_by_email(data['email'])
        token: Optional[str] = request.headers.get('Authorization', None)

        # Update user data only if auth user has the same email as the one in the questionnaire
        if user and user.id == User.decode_auth_token(token):  # type: ignore
            user.first_name = data['first_name']
            user.address = data['address']
            user.children = data['children']
            user.occupation = data['occupation']
            user.update()

        # Get insurance recommendation
        insurance_list = Insurance.get_recommendation(data['occupation'], data['children'])
    except Exception:
        return make_response(jsonify({'message': 'Failed to get recommendation.'}), 500)

    response_object = {'recommendations': insurance_schema.dump(insurance_list, many=True)}
    return make_response(jsonify(response_object), 200)


@insurance_bp.route('/insurances', methods=('POST',))
@validate_input(schema=insurance_list_schema)
def insurances() -> Response:
    """Insert new insurances.

    :return: JSON response
    """
    # Get data from the request
    data = request.get_json()

    try:
        count = 0
        for insurance in data['insurances']:
            # Insert new insurance to the database if not already registered
            if not Insurance.find_insurance(insurance['name']):
                Insurance(insurance['name'], insurance['monthly_price']).create()
                count += 1
    except Exception:
        return make_response(jsonify({'message': 'Failed to save new insurances.'}), 500)

    insurance_str = 'insurance' if count == 1 else 'insurances'

    return make_response(jsonify({'message': f'{count} {insurance_str} successfully saved.'}), 200)
