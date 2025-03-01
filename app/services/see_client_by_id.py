"""Клиент по ID"""

from flask import Response, redirect, render_template, url_for
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError

from .. models import Client
from .. schema import ClientSchema


def get_client_id_for_search(form) -> Response | str:
    """Перенаправляет ID клиента, или шаблонизирует ошибку"""
    if form.validate_on_submit():
        client_id = form.client_id.data
        return redirect(url_for("get_client_by_id", client_id=client_id))
    return render_template(
        "client_by_id.html", form=form)


def get_client_data_by_id(form, client_id) -> str:
    """Шаблонизирует ответ на запрос клиента по ID"""
    try:
        client = Client.select_client_by_id(idc=client_id)
        schema = ClientSchema()
        client_data = schema.dump(client)
        return render_template(
            "client_by_id.html", client=client_data, form=form
        )
    except InvalidRequestError as exc:
        return render_template(
            "client_by_id.html", error=str(exc), form=form
        )

    except SQLAlchemyError as sql:
        return render_template(
            "client_by_id.html", error=str(sql), form=form
        )
    except ValueError as val:
        return render_template(
            "client_by_id.html", error=str(val), form=form
        )
