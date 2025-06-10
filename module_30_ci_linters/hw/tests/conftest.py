"""
Модуль с настройками для тестирования с pytest
"""

from datetime import datetime

import pytest

from module_30_ci_linters.homework.hw1.app.models import Client, ClientParking, Parking
from module_30_ci_linters.homework.hw1.main import create_app
from module_30_ci_linters.homework.hw1.main import db as _db


@pytest.fixture
def app():
    """Приложение с настройками для запуска тестирования"""
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        client_1 = Client(
            name="name",
            surname="surname",
            credit_card="credit_card",
            car_number="car_number",
        )
        client_2 = Client(
            name="name",
            surname="surname",
            credit_card="credit_card",
            car_number="car_number",
        )
        client_3 = Client(
            name="name", surname="surname", credit_card=None, car_number="car_number"
        )
        parking_1 = Parking(
            address="address", opened=1, count_places=10, count_available_places=5
        )
        parking_2 = Parking(
            address="address", opened=0, count_places=5, count_available_places=5
        )
        parking_3 = Parking(
            address="address", opened=1, count_places=5, count_available_places=0
        )
        client_parking_1 = ClientParking(
            client_id=1, parking_id=1, time_in=datetime.now(), time_out=datetime.now()
        )
        client_parking_2 = ClientParking(
            client_id=3,
            parking_id=1,
            time_in=datetime.now(),
        )

        _db.session.add_all([client_1, client_2, client_3])
        _db.session.add_all([parking_1, parking_2, parking_3])
        _db.session.add_all([client_parking_1, client_parking_2])
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app_client):
    """Фикстура клиент"""
    client_test = app_client.test_client()
    yield client_test


@pytest.fixture
def db(app_client):
    """Фикстура бд"""
    with app_client.app_context():
        yield _db
