"""Регистрация маршрутов приложения"""

from flask import render_template

from services import (add_client, add_parking, enter_client_parking,
                      out_client_parking, see_all_client_parking,
                      see_client_by_id, see_clients, see_parking)
from validate import (ClientAddForm, ClientParkingForm, ClientSearchForm,
                      ParkingAddForm)


def register_routes(app):
    """Регистрирует маршруты Flask-приложения."""
    @app.route("/", methods=["GET"])
    def index() -> tuple[str, int]:
        """Отображает главную страницу."""
        return render_template("index.html"), 200

    @app.route("/add_client", methods=["GET", "POST"])
    def add_or_update_client() -> str:
        """Добавляет или обновляет клиента."""
        form = ClientAddForm()
        return (
            add_client
            .add_or_update_client_for_parking(form=form)
        )

    @app.route("/add_parking", methods=["GET", "POST"])
    def add_or_update_parking() -> str:
        """Добавляет или обновляет парковку."""
        form = ParkingAddForm()
        return (
            add_parking
            .add_or_update_parking_places(form=form)
        )

    @app.route("/clients", methods=["GET"])
    def get_clients() -> str:
        """Отображает список клиентов."""
        return see_clients.see_all_clients_for_parking()

    @app.route("/client_search", methods=["GET", "POST"])
    def client_search() -> str:
        """Ищет клиента."""
        form = ClientSearchForm()
        return (see_client_by_id
                .get_client_id_for_search(form=form))

    @app.route("/client/<int:client_id>", methods=["GET"])
    def get_client_by_id(client_id: int):
        """Отображает клиента по ID."""
        form = ClientSearchForm()
        return (see_client_by_id
                .get_client_data_by_id(
                 form=form, client_id=client_id)
                )

    @app.route("/parking", methods=["GET"])
    def get_all_parking() -> str:
        """Отображает список парковок."""
        return see_parking.see_all_parking_places()

    @app.route("/enter_client_parking", methods=["POST", "GET"])
    def add_or_update_client_parking() -> str:
        """Регистрирует въезд клиента на парковку."""
        form = ClientParkingForm()
        return (enter_client_parking
                .put_the_client_for_parking(form=form))

    @app.route(
        "/out_client_parking", methods=["GET", "POST", "PATCH"]
    )
    def patch_out_client_parking() -> str:
        """Регистрирует выезд клиента с парковки."""
        form = ClientParkingForm()
        return (out_client_parking
                .out_and_pay_client_parking(form=form))

    @app.route("/client_parking", methods=["GET"])
    def get_client_parking() -> str:
        """Отображает информацию о парковке клиента."""
        return (see_all_client_parking
                .see_all_client_parking())
