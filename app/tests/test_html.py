"""Тесты html"""

import pytest


@pytest.mark.html
def test_index_template_rendered(
        _client, captured_templates
):
    """Проверяет, что рендерится правильный шаблон."""
    response = _client.get("/")
    assert response.status_code == 200
    assert len(captured_templates) > 0
    template_name, _ = captured_templates[-1]
    assert template_name.name == "index.html"


@pytest.mark.html
def test_add_client_template_rendered(
        _client, captured_templates
):
    """Проверяем шаблон для добавления клиента"""
    response = _client.post(
        "/add_client",
        data={
            "name": "Иван",
            "surname": "Лаптев",
            "credit_card": "1234 5678 9012 3456",
            "car_number": "А123BC77",
        },
    )
    assert response.status_code == 200
    assert len(captured_templates) > 0
    template_name, _ = captured_templates[-1]
    assert template_name.name == "add_client.html"


@pytest.mark.html
def test_add_parking_template_rendered(
        _client, captured_templates
):
    """Проверяем шаблон для добавления клиента"""
    response = _client.post(
        "/add_parking",
        data={
            "address": "Москва, Абрамцевская, 30",
            "opened": True,
            "count_place": 30,
            "count_available_places": 5,
        },
    )
    assert response.status_code == 200
    assert len(captured_templates) > 0
    template_name, _ = captured_templates[-1]
    assert template_name.name == "add_parking.html"


@pytest.mark.html
def test_get_clients_template_rendered(
        _client, captured_templates
):
    """Проверяет, что при получении клиентов рендерится правильный шаблон."""
    response = _client.get("/clients")
    assert response.status_code == 200
    assert len(captured_templates) > 0
    template_name, _ = captured_templates[-1]
    assert template_name.name == "all_clients.html"


@pytest.mark.html
def test_get_parking_template_rendered(
        _client, captured_templates
):
    """Проверяет, что при получении парковок рендерится правильный шаблон."""
    response = _client.get("/parking")
    assert response.status_code == 200
    assert len(captured_templates) > 0
    template_name, _ = captured_templates[-1]
    assert template_name.name == "all_parking.html"


@pytest.mark.html
def test_add_client_parking_template_rendered(
        _client, captured_templates
):
    """Проверяем шаблон для добавления клиент-паркинга"""
    response = _client.post(
        "/enter_client_parking",
        data={
            "client_id": 1,
            "parking_id": 1,
            "time_in": "2025-03-02 07:00:00"
        },
    )
    assert response.status_code == 200
    assert len(captured_templates) > 0
    template_name, _ = captured_templates[-1]
    assert template_name.name == "client_parking_result.html"


@pytest.mark.html
def test_add_out_client_parking_template_rendered(
        _client, captured_templates
):
    """Проверяем шаблон для выезда из парковки"""
    response = _client.post(
        "/out_client_parking",
        data={
            "client_id": 1,
            "parking_id": 1,
            "time_out": "2025-03-02 15:00:00"
        },
    )
    assert response.status_code == 200
    assert len(captured_templates) > 0
    template_name, _ = captured_templates[-1]
    assert template_name.name == "out_client_parking.html"


@pytest.mark.html
def test_see_client_parking(
        _client, captured_templates
):
    """Проверяет шаблон базы клиентов"""
    response = _client.get("/client_parking")
    assert response.status_code == 200
    assert len(captured_templates) > 0
    template_name, _ = captured_templates[-1]
    assert not template_name.name == "not.html"
    assert template_name.name == "all_client_parking.html"
