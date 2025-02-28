"""Тест окончания паркинга"""

import pytest


@pytest.mark.parking
def test_client_parking_out(_client):
    """Тест выезда из парковок"""
    # Провокация выезда клиента с ID 2 из паркинга с ID 2
    data_out = {
        "client_id": 1,
        "parking_id": 2,
        "time_out": "2025-03-02 15:00:00"
    }
    response1 = _client.post(
        "/out_client_parking",
        data=data_out,
        content_type="application/x-www-form-urlencoded",
    )
    assert response1.status_code == 200

    # Выезд клиента с ID 1 из паркинга с  ID 1
    data_out = {
        "client_id": 1,
        "parking_id": 1,
        "time_out": "2025-03-02 15:00:00"
    }
    response2 = _client.post(
        "/out_client_parking",
        data=data_out,
        content_type="application/x-www-form-urlencoded",
    )
    assert response2.status_code == 200

    # Провокация выезда клиента с ID 3 без заполненной формы
    data_out = {
        "client_id": 3,
        "parking_id": 2,
        "time_out": "2025-03-02 15:00:00"
    }
    response3 = _client.post(
        "/out_client_parking",
        data=data_out,
        content_type="application/x-www-form-urlencoded",
    )
    assert response3.status_code == 200
