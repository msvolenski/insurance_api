"""Insurance Model."""

from __future__ import annotations
from typing import List, Optional

from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf, Range
from sqlalchemy.orm.exc import NoResultFound

from application import db


class QuestionnaireSchema(Schema):
    """Schema for validation of Questionnaire fields."""

    first_name = fields.Str(required=True, validate=Length(min=3, max=20))
    address = fields.Str(required=True, validate=Length(min=5, max=50))
    children = fields.Int(required=False, default=0, validate=Range(min=0))
    occupation = fields.Str(
        required=True, validate=OneOf(choices=['employed', 'self-employed', 'student'])
    )
    email = fields.Email(required=True)


class InsuranceSchema(Schema):
    """Schema for validation of Insurance fields."""

    name = fields.Str(required=True, validate=Length(min=3, max=50))
    monthly_price = fields.Float(required=True, validate=Range(min=0.0))


class InsuranceListSchema(Schema):
    """Schema for validation of a list of Insurance fields."""

    insurances = fields.List(
        fields.Nested(InsuranceSchema(only=('name', 'monthly_price')))
    )


class Insurance(db.Model):  # type: ignore
    """Insurance database model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    monthly_price = db.Column(db.Float, nullable=False)

    def __init__(self, name: str, monthly_price: float):
        """Initialize Insurance object.

        :param name: Type of insurance (name)
        :param monthly_price: Monthly price of the insurance
        """
        self.name = name
        self.monthly_price = monthly_price

    def create(self) -> Insurance:
        """Create insurance and save to database.

        :return: Insurance object
        """
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def find_insurance(name: str) -> Optional[Insurance]:
        """Search insurance by name.

        :param name: Insurance name
        :return: Insurance model or None
        """
        try:
            insurance = Insurance.query.filter_by(name=name).one()
        except NoResultFound:
            insurance = None

        return insurance  # type: ignore

    @staticmethod
    def get_recommendation(occupation: str, children: int) -> List[Insurance]:
        """Search for specific insurance for different customer realities.

        :param occupation: Occupation of the customer
        :param children: Number of children the customer has
        :return: List of recommended insurances for this customer
        """
        recommendation = []
        if occupation.lower() == 'employed':
            recommendation.append(
                Insurance.query.filter(Insurance.name.contains('Private')).first()
            )
            recommendation.append(
                Insurance.query.filter(Insurance.name.contains('Household')).first()
            )
        elif occupation.lower() == 'student':
            recommendation.append(
                Insurance.query.filter(Insurance.name.contains('Expat')).first()
            )
        else:
            recommendation.append(
                Insurance.query.filter(Insurance.name.contains('Public')).first()
            )
            recommendation.append(
                Insurance.query.filter(Insurance.name.contains('Legal')).first()
            )

        if children:
            recommendation.append(
                Insurance.query.filter(Insurance.name.contains('Life')).first()
            )

        return recommendation
