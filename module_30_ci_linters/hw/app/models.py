from typing import Any, Dict

from sqlalchemy import UniqueConstraint

from .database import db


class Client(db.Model):
    """
    Модель таблицы client
    """

    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    def __repr__(self):
        return (
            f"Client id: {self.id}, "
            f"name: {self.name}, "
            f"surname: {self.surname}, "
            f"credit_card: {self.credit_card}, "
            f"car_number: {self.car_number}"
        )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    """
    Модель таблицы parking
    """

    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (
            f"Parking id: {self.id}, address: {self.address}, opened: {self.opened}, "
            f"count_places: {self.count_places}, count_available_places: {self.count_available_places}"
        )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):
    """
    Модель таблицы client_parking
    """

    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"))

    __table_args__ = (
        UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )

    client = db.relationship("Client", backref="client_parking")
    parking = db.relationship("Parking", backref="client_parking")

    def __repr__(self):
        return (
            f"Parking id: {self.id}, time_in: {self.time_in}, time_out: {self.time_out}"
        )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}