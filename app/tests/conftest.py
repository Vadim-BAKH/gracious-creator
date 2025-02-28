"""Конфигурация для pytest."""

import pytest
from flask.signals import template_rendered

from database import SECRET_KEY, TEST_DB_URI
from flask_main import create_app
from log import logger
from models import Client, ClientParking, Parking
from models import db as db_test


def add_test_data(db_session):
    """Добавляет тестовые данные в базу данных."""
    try:
        for model in [ClientParking, Parking, Client]:
            db_session.query(model).delete()

        client = Client(
            name="Денис",
            surname="Петров",
            credit_card="5555 5555 5555 5555",
            car_number="Х777ХА777",
        )
        parking = Parking(
            address="Москва, Песчаная, 20",
            opened=True,
            count_place=30,
            count_available_places=1,
        )

        db_session.add(client)
        db_session.add(parking)
        db_session.flush()

        client_parking = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in="2025-03-01 10:00:00",
            time_out="2025-03-01 15:15:35",
        )

        db_session.add(client_parking)
        db_session.commit()
    except Exception as exc:
        logger.error(f"Error adding test data: {exc}")
        db_session.rollback()
        raise


def pytest_addoption(parser):
    """Добавляет опцию командной строки для указания URL базы данных."""
    parser.addoption(
        "--db_url",
        action="store",
        default=TEST_DB_URI,
        help="URL базы данных для использования в тестах.",
    )


@pytest.fixture(scope="session")
def test_db_url(request):
    """Фикстура для получения URL базы данных."""
    db_url = request.config.getoption("--db_url")
    return db_url


@pytest.fixture(scope="session")
def test_app(test_db_url):
    """Создает тестовую конфигурацию Flask и инициализирует базу данных."""
    _test_app = create_app()
    _test_app.config["TESTING"] = True
    _test_app.config["SQLALCHEMY_DATABASE_URI"] = test_db_url
    _test_app.config["SECRET_KEY"] = SECRET_KEY
    _test_app.config["WTF_CSRF_ENABLED"] = False

    with _test_app.app_context():
        db_test.create_all()

    yield _test_app

    with _test_app.app_context():
        db_test.session.remove()
        db_test.drop_all()


@pytest.fixture(scope="function")
def test_db_session(test_app):
    """Предоставляет доступ к сессии базы данных."""
    with test_app.app_context():
        db_test.session.begin()
        yield db_test.session
        db_test.session.rollback()
        db_test.session.close()


@pytest.fixture(scope="function", autouse=True)
def setup_test_db(test_db_session, test_app):
    """Добавляет тестовые данные и очищает базу данных."""
    with test_app.app_context():
        add_test_data(db_session=test_db_session)
        yield


@pytest.fixture(scope="function")
def _client(test_app):
    """Создает тестовый клиент для отправки запросов к приложению."""
    with test_app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def test_database(test_app):
    """Предоставляет доступ к базе данных."""
    with test_app.app_context():
        yield db_test


@pytest.fixture(scope="function")
def captured_templates(test_app):
    """Перехватывает рендеринг шаблонов."""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
        logger.info(f"Used sender: {sender}; extra: {extra}")

    template_rendered.connect(record, test_app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, test_app)
