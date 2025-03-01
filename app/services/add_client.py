"""Добавление клиента"""

from flask import render_template
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError

from .. models import Client


def add_or_update_client_for_parking(form) -> str:
    """
    Шаблонизирует ответ на запрос
    добавления клиента
    """

    if form.validate_on_submit():
        client_data = {
            "name": form.name.data,
            "surname": form.surname.data,
            "credit_card": form.credit_card.data,
            "car_number": form.car_number.data,
        }

        try:
            client = Client.add_or_update_client(
                data_client=client_data
            )
            return render_template(
                "add_client.html",
                form=form,
                success=True,
                client=client[0],
            )
        except ValueError as val:
            return render_template(
                "add_client.html",
                form=form,
                error=str(val)
            )
        except InvalidRequestError as exc:
            return render_template(
                "add_client.html",
                form=form,
                error=str(exc)
            )
        except SQLAlchemyError as sql:
            return render_template(
                "add_client.html",
                form=form,
                error=str(sql)
            )

    return render_template(
        "add_client.html",
        form=form
    )
