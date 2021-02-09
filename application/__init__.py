"""Create Application."""

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# Globally accessible libraries
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_object: str = 'config.Develop') -> Flask:
    """Initialize core application.

    :param config_object: Application settings
    :return: Application instance
    """
    # Start application
    app = Flask(__name__, instance_relative_config=False)

    # Load configuration
    if app.env == 'production':
        app.config.from_object('config.Production')
    else:
        app.config.from_object(config_object)

    # Configure application
    initialize_plugins(app)
    register_blueprints(app)

    return app


def initialize_plugins(app: Flask):
    """Setup used plugins.

    :param app: Application instance
    :return:
    """
    # Initialize plugins
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app: Flask):
    """Setup used blueprints.

    :param app: Application instance
    :return:
    """
    # Include routes
    from application.blueprints.auth import auth_bp
    from application.blueprints.insurance import insurance_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(insurance_bp)
