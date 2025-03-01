"""
WSGI-конфигурация для приложения
"""


from .flask_main import create_app

app = create_app()
