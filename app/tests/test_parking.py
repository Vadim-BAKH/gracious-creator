"""Тесты парковок"""


def test_add_parking(_client):
    """Тест создания парковки c 1 свободным местом"""
    data_parking = {
        "address": "Москва, Абрамцевская, 20",
        "opened": True,
        "count_place": 30,
        "count_available_places": 1,
    }
    response = _client.post(
        "/add_client",
        data=data_parking,
        content_type="application/x-www-form-urlencoded",
    )
    assert response.status_code == 200
