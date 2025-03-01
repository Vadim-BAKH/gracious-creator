"""Фэйк - фабрика"""

from random import choice, randint, randrange

from factory import Faker, LazyAttribute, alchemy

from .. log import logger
from .. models import Client, Parking, db


def create_car_number_random(obj) -> str:
    """Собираем случайный номер машины"""
    letters = "АВЕКМНОРСТУХ"
    car_number = (
        f"{choice(letters)}"
        f"{randint(100, 999)}"
        f"{choice(letters) * 3}"
        f"{randint(1, 999)}"
    )
    logger.info(f"Creating obj: {obj}")
    return car_number


def create_credit_card_random(obj) -> str:
    """Собираем случайный номер карты"""
    number = randint(0, 9)
    credit_card_number = f"{number * 4} {number * 4} {number * 4} {number * 4}"
    logger.info(f"Creating obj: {obj}")
    return credit_card_number


class ClientFactory(alchemy.SQLAlchemyModelFactory):
    """Фабрика для создания объектов Client."""
    class Meta:
        """Метаданные для фабрики Client."""
        model = Client
        sqlalchemy_session = db.session

    name = Faker("first_name")
    surname = Faker("last_name")
    credit_card = LazyAttribute(create_credit_card_random)
    car_number = LazyAttribute(create_car_number_random)


class ParkingFactory(alchemy.SQLAlchemyModelFactory):
    """Фабрика для создания объектов Parking."""
    class Meta:
        """Метаданные для фабрики Parking."""
        model = Parking
        sqlalchemy_session = db.session

    address = Faker("address")
    opened = Faker("boolean")
    count_place = LazyAttribute(
        lambda obj: randrange(10, 51)
    )
    count_available_places = LazyAttribute(
        lambda num: randrange(0, num.count_place)
    )
