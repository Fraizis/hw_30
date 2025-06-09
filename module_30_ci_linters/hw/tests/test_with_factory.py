from ..app.models import Client, Parking
from .factories import ClientFactory, ParkingFactory


def test_create_client(app, db):
    client_create = ClientFactory()
    db.session.commit()
    assert client_create.id is not None
    assert len(db.session.query(Client).all()) == 4


def test_create_parking(client, db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id is not None
    assert len(db.session.query(Parking).all()) == 4
