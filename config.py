"""Flask config class."""

import os

from dotenv import load_dotenv


BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class Production:
    """Set production application configuration."""

    # General Config
    TESTING = os.getenv('TESTING')
    DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')


class Develop:
    """Set development application configuration."""

    # General Config
    TESTING = os.getenv('DEV_TESTING')
    DEBUG = os.getenv('DEV_DEBUG')
    SECRET_KEY = os.getenv('DEV_SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('DEV_SQLALCHEMY_TRACK_MODIFICATIONS')


class Test:
    """Set development application configuration."""

    # General Config
    TESTING = os.getenv('DEV_TESTING')
    DEBUG = os.getenv('DEV_DEBUG')
    SECRET_KEY = os.getenv('TEST_SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('DEV_SQLALCHEMY_TRACK_MODIFICATIONS')
