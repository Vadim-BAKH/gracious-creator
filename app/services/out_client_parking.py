"""Выезд с парковки"""

from flask import render_template
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError

from app.models import Client, ClientParking, Parking
from app.utils import process_client_parking_form


def out_and_pay_client_parking(form) -> str:
    """
    Шаблонизирует ответ на запрос окончания парковки клиента
    """
    if form.validate_on_submit():
        client_id, parking_id = process_client_parking_form(form=form)
        try:

            Client.check_car_number_and_credit_card(idc=client_id)
            Parking.select_parking_by_id(idp=parking_id)
            ClientParking.search_client_in_parking_out(
                idc=client_id, idp=parking_id
            )
            Parking.test_update_parking_out(idp=parking_id)

            result = ClientParking.update_time_out_client_parking(
                idc=client_id, idp=parking_id
            )

            return render_template(
                "out_client_parking.html",
                form=form,
                client_id=result[0][0],
                parking_id=result[0][1],
                time_out=result[0][2],
                parking_duration=result[0][3],
                check=result[0][4],
            )

        except InvalidRequestError as exc:
            return render_template(
                "out_client_parking.html", form=form, error=str(exc)
            )
        except SQLAlchemyError as sql:
            return render_template(
                "out_client_parking.html", form=form, error=str(sql)
            )
        except ValueError as val:
            return render_template(
                "out_client_parking.html", form=form, error=str(val)
            )

    return render_template(
        "out_client_parking.html", form=form
    )
