"""Тесты фэйков клиента"""

import pytest

from .. factories.factories import ClientFactory
from .. models import Client


@pytest.mark.fake
def test_create_client_with_factory(test_database):
    """Тестируем создание клиента с factory-boy"""
    test_database.session.rollback()
    initial_client_count = Client.query.count()
    client = ClientFactory()
    test_database.session.commit()
    assert client.id is not None
    assert Client.query.count() == initial_client_count + 1
    assert client.name is not None
    assert client.surname is not None
    assert client.car_number is not None
