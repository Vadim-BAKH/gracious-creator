"""Параметрический тест GET"""

import pytest


@pytest.mark.parametrize(
    "route", ["/", "/clients", "/parking", "/client_parking"]
)
def test_get_methods(_client, route):
    """Проверяет, что все GET-методы возвращают код 200."""

    response = _client.get(route)
    assert response.status_code == 200
