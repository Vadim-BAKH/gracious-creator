"""Тест конфигурации"""

from .. database import SECRET_KEY


def test_app_config(test_app):
    """Тест конфигурации"""
    assert not test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    assert not test_app.config["DEBUG"]
    assert test_app.config["TESTING"]
    assert test_app.config["SECRET_KEY"] == SECRET_KEY
