"""Заезд на парковку"""

from flask import render_template
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError

from app.models import Client, ClientParking, Parking
from app.utils import process_client_parking_form


def put_the_client_for_parking(form) -> str:
    """
    Шаблонизирует ответ на запрос создания клиент-паркинга
    """
    client_id, parking_id = process_client_parking_form(form=form)
    if client_id and parking_id:
        try:
            # Проверка и выполнение операций
            Client.select_client_by_id(client_id)
            Parking.select_parking_by_id(parking_id)
            ClientParking.search_client_in_parking_enter(idc=client_id)

            Parking.test_update_parking_enter(idp=parking_id)
            result = ClientParking.insert_or_update_client_parking(
                idc=client_id,
                idp=parking_id,
            )

            return render_template(
                "client_parking_result.html", form=form, result=result[0]
            )
        except InvalidRequestError as exc:
            return render_template(
                "client_parking_result.html",
                form=form,
                error=str(exc)
            )

        except SQLAlchemyError as sql:
            return render_template(
                "client_parking_result.html", form=form, error=str(sql)
            )
        except ValueError as val:
            return render_template(
                "client_parking_result.html", form=form, error=str(val)
            )

    # Если форма не прошла валидацию, возвращаем её обратно
    return render_template("client_parking_result.html", form=form)
