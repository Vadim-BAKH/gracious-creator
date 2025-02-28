"""
Вспомогательные функции
"""


def process_client_parking_form(form):
    """Обрабатывает данные формы клиент-паркинга."""
    if form.validate_on_submit():
        client_parking_data = {
            "client_id": form.client_id.data,
            "parking_id": form.parking_id.data,
        }
        client_id = client_parking_data.get("client_id")
        parking_id = client_parking_data.get("parking_id")
        return client_id, parking_id
    return None, None
