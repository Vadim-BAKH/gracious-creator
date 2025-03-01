"""Тесты фэйков парковок"""

import pytest

from .. factories.factories import ParkingFactory
from .. models import Parking


@pytest.mark.fake
def test_create_parking_with_factory(test_database):
    """Тестируем создание парковки с factory-boy"""
    test_database.session.rollback()
    initial_client_count = Parking.query.count()
    parking = ParkingFactory()
    test_database.session.commit()

    assert parking.id is not None
    assert Parking.query.count() == initial_client_count + 1
    assert isinstance(parking.opened, bool)
    assert parking.address is not None
    assert parking.count_place >= 10
    assert parking.count_available_places >= 0
