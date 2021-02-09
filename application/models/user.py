"""User Model."""

from __future__ import annotations
import datetime
from typing import Optional

from flask import current_app
import jwt
from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf, Range
from sqlalchemy.orm.exc import NoResultFound

from application import db


class UserSchema(Schema):
    """Schema for validation of User fields."""

    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=8, max=30))
    first_name = fields.Str(required=False, validate=Length(min=3, max=20))
    address = fields.Str(required=False, validate=Length(min=5, max=50))
    children = fields.Int(required=False, default=0, validate=Range(min=0))
    occupation = fields.Str(
        required=False, validate=OneOf(choices=['employed', 'self-employed', 'student'])
    )


class User(db.Model):  # type: ignore
    """User database model."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    occupation = db.Column(db.String(30), nullable=True)
    children = db.Column(db.Integer, nullable=True, default=0)

    def __init__(self, email: str, password: str):
        """Initialize User object.

        :param email: User email
        :param password: User password
        """
        self.email = email
        self.password = password

    def create(self) -> User:
        """Create user and save to database.

        :return: User object
        """
        db.session.add(self)
        db.session.commit()
        return self

    def update(self) -> User:
        """Update user and save to database.

        :return: User object
        """
        db.session.commit()
        return self

    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        """Search user by email.

        :param email: Email to search for
        :return: User instance
        """
        try:
            user = User.query.filter_by(email=email).one()
        except NoResultFound:
            user = None
        return user  # type: ignore

    @staticmethod
    def encode_auth_token(user_id: int) -> str:
        """Generate authentication token.

        :param user_id: User id
        :return: Token string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def decode_auth_token(auth_token: str) -> int:
        """Decode authentication token.

        :param auth_token: Token string
        :return: Token owner user id
        """
        try:
            payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload['sub']  # type: ignore
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError('Invalid token. Please log in again.')
