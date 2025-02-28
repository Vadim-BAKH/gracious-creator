"""Все клиенты"""

from flask import render_template
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError

from models import Client
from schema import ClientSchema


def see_all_clients_for_parking() -> str:
    """Шаблонизирует ответ на запрос всех клиентов"""
    try:
        clients = Client.select_clients()
        schema = ClientSchema(many=True)
        clients_data = schema.dump(clients)

        return render_template(
            "all_clients.html", clients=clients_data
        )
    except InvalidRequestError as exc:
        return render_template(
            "all_clients.html", error=str(exc)
        )
    except ValueError as val:
        return render_template(
            "all_clients.html", error=str(val)
        )
    except SQLAlchemyError as sql:
        return render_template(
            "all_clients.html", error=str(sql)
        )
