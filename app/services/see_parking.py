"""Все парковки"""

from flask import render_template
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError

from app.models import Parking
from app.schema import ParkingSchema


def see_all_parking_places() -> str:
    """
    Шаблонизирует ответ на запрос базы клиент-паркинга
    """
    try:
        all_parking_data = Parking.select_all_parking()
        schema = ParkingSchema(many=True)
        all_parking = schema.dump(all_parking_data)
        return render_template(
            "all_parking.html", places=all_parking
        )
    except InvalidRequestError as exc:
        return render_template(
            "all_parking.html", error=str(exc)
        )
    except ValueError as val:
        return render_template(
            "all_parking.html", error=str(val)
        )
    except SQLAlchemyError as sql:
        return render_template(
            "all_parking.html", error=str(sql)
        )
