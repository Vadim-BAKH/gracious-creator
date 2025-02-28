"""Тесты парковок"""

import pytest


@pytest.mark.parking
def test_enter_client_parking(_client):
    """Тесты для создания клиент паркинга"""
    # Клиент с ID 1 заехал на парковку с ID 1
    data_enter = {
        "client_id": 1,
        "parking_id": 1,
        "time_in": "2025-03-02 10:00:00"
    }
    response1 = _client.post(
        "/enter_client_parking",
        data=data_enter,
        content_type="application/x-www-form-urlencoded",
    )
    assert response1.status_code == 200

    # Провокация одновременного заезда клиента с ID 1 на парковку с ID 2
    data_enter = {
        "client_id": 1,
        "parking_id": 2,
        "time_in": "2025-03-02 10:00:00"}
    response2 = _client.post(
        "/enter_client_parking",
        data=data_enter,
        content_type="application/x-www-form-urlencoded",
    )
    assert response2.status_code == 200

    # Провокация заезда на парковку с ID 1, где больше нет мест
    data_enter = {
        "client_id": 2,
        "parking_id": 1,
        "time_in": "2025-03-02 10:00:00"
    }
    response3 = _client.post(
        "/enter_client_parking",
        data=data_enter,
        content_type="application/x-www-form-urlencoded",
    )
    assert response3.status_code == 200

    # Клиент с ID 3 заехал на парковку c ID 2
    data_enter = {
        "client_id": 3,
        "parking_id": 2,
        "time_in": "2025-03-02 10:00:00"
    }
    response4 = _client.post(
        "/enter_client_parking",
        data=data_enter,
        content_type="application/x-www-form-urlencoded",
    )
    assert response4.status_code == 200

    # Провокация на клиента с несуществующим ID
    data_enter = {"client_id": 200, "parking_id": 2}
    response5 = _client.post(
        "/enter_client_parking",
        data=data_enter,
        content_type="application/x-www-form-urlencoded",
    )
    assert response5.status_code == 200
