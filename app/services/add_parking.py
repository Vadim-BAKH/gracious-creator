"""Добавление парковки"""

from flask import render_template
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError

from .. models import Parking


def add_or_update_parking_places(form):
    """
    Шаблонизирует ответ на запрос
    создания парковка
    """
    if form.validate_on_submit():
        parking_data = {
            "address": form.address.data,
            "opened": form.opened.data,
            "count_place": form.count_place.data,
            "count_available_places":
                form.count_available_places.data,
        }
        try:
            parking = (Parking
                       .insert_or_update_parking(
                        data_parking=parking_data)
                       )
            return render_template(
                "add_parking.html",
                form=form,
                success=True,
                parking=parking[0],
            )
        except InvalidRequestError as exc:
            return render_template(
                "add_parking.html",
                form=form,
                error=str(exc)
            )
        except ValueError as val:
            return render_template(
                "add_parking.html",
                form=form,
                error=str(val))
        except SQLAlchemyError as sql:
            return render_template(
                "add_parking.html",
                form=form,
                error=str(sql)
            )

    return render_template(
        "add_parking.html",
        form=form
    )
