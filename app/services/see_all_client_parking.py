"""История парковок"""

from flask import render_template
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError

from models import ClientParking
from schema import ClientParkingSchema


def see_all_client_parking() -> str:
    """Шаблонизирует ответ на запрос всех клиентов"""
    try:
        client_parking = ClientParking.select_all_client_parking()
        schema = ClientParkingSchema(many=True)
        client_parking_data = schema.dump(client_parking)

        return render_template(
            "all_client_parking.html", result=client_parking_data
        )
    except InvalidRequestError as exc:
        return render_template(
            "all_client_parking.html", error=f"Ошибка сервера: {str(exc)}"
        )

    except ValueError as val:
        return render_template(
            "all_client_parking.html", error=str(val)
        )
    except SQLAlchemyError as sql:
        return render_template(
            "all_client_parking.html",
            error=str(sql)
        )
