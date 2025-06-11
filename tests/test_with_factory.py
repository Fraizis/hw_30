"""
Тесты с использованием factory boy
"""

from app.models import Client, Parking

from .factories import ClientFactory, ParkingFactory


def test_create_client(db):
    """Тест создание клиента"""
    client_create = ClientFactory()
    db.session.commit()
    assert client_create.id is not None
    assert len(db.session.query(Client).all()) == 4


def test_create_parking(db):
    """Тест создание парковки"""
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id is not None
    assert len(db.session.query(Parking).all()) == 4
