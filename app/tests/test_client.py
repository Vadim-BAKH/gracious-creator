"""Тест клиентов"""


def test_client_creation_and_search(_client):
    """Тест создания клиента и поиска клиента по ID."""

    # Тест создания клиента с ID 2
    first_data = {
        "name": "Иван",
        "surname": "Иванов",
        "credit_card": "1234 5678 9012 3456",
        "car_number": "А123BC77",
    }
    response = _client.post(
        "/add_client", data=first_data,
        content_type="application/x-www-form-urlencoded"
    )
    assert response.status_code == 200

    # тест провокация не создаст клиента
    first_data = {
        "name": "Иван",
        "credit_card": "1234 5678 9012 3456",
        "car_number": "А123BC77",
    }
    response = _client.post(
        "/add_client", data=first_data,
        content_type="application/x-www-form-urlencoded"
    )
    assert response.status_code == 200

    # Передадим в форму ID 2
    search_id = {"client_id": 2}
    response = _client.post(
        "/client_search",
        data=search_id,
        content_type="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Получим клиента по ID 2
    client_id = 2
    response = _client.get(f"/client/{client_id}")
    assert response.status_code == 200

    # Создадим клиента с ID 3 без необязательных полей
    second_data = {
        "name": "Пётр",
        "surname": "Лукин",
    }
    response = _client.post(
        "/add_client",
        data=second_data,
        content_type="application/x-www-form-urlencoded",
    )
    assert response.status_code == 200

    # Передадим в форму ID 3
    search_id = {"client_id": 3}
    response = _client.post(
        "/client_search",
        data=search_id,
        content_type="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Получим клиента по ID 3
    client_id = 3
    response = _client.get(f"/client/{client_id}")
    assert response.status_code == 200

    search_id = {"client_id": 55}
    response = _client.post(
        "/client_search",
        data=search_id,
        content_type="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Провокация на несуществующий ID
    client_id = 55
    response = _client.get(f"/client/{client_id}")
    assert response.status_code == 200
