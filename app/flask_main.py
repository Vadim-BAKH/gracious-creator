"""Фабрика приложения Flask"""

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .database import DATABASE_URI, SECRET_KEY
from .log import logger
from .models import db
from .register_routes import register_routes

csrf = CSRFProtect()


def create_app():
    """Фабрика для создания экземпляра Flask приложения."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    @app.teardown_appcontext
    def finish(exception=None):
        logger.info(f"Finishing with {exception}")
        db.session.remove()

    register_routes(app)

    return app
