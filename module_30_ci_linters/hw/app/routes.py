from datetime import datetime
from typing import List

import sqlalchemy.exc
from flask import Blueprint, jsonify, request

from .models import Client, ClientParking, Parking, db

url_blueprint = Blueprint(
    "url",
    __name__,
)


@url_blueprint.route("/clients", methods=["GET"])
def get_all_clients():
    """
    Получение клиентов
    """
    clients: List[Client] = db.session.query(Client).all()
    clients_list = [u.to_json() for u in clients]
    return jsonify(clients_list), 200


@url_blueprint.route("/clients/<int:client_id>", methods=["GET"])
def get_client_by_id(client_id: int):
    """
    Получение клиента по ид
    """
    client: Client = db.session.get(Client, client_id)
    if client:
        return jsonify(client.to_json()), 200

    return "No such client", 404


@url_blueprint.route("/clients", methods=["POST"])
def create_client():
    """
    Создание нового клиента

    Пример:
    {
    'name':'name',
    'surname':'surname',
    'credit_card':'1235656',
    'car_number':'3454dgf'
    }
    """
    data = request.json
    new_client = Client(
        name=data["name"],
        surname=data["surname"],
        credit_card=data.get("credit_card", None),
        car_number=data.get("car_number", None),
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify(new_client.to_json()), 201


@url_blueprint.route("/parking/<int:parking_id>", methods=["GET"])
def get_parking_by_id(parking_id: int):
    """
    Получение парковки по ид
    """
    parking: Parking = db.session.get(Parking, parking_id)
    if parking:
        return jsonify(parking.to_json()), 200

    return "No such parking", 404


@url_blueprint.route("/parking", methods=["POST"])
def create_parking():
    """
    Создание новой парковки

    Пример:
    {
    'address':'address',
    'opened':'1',
    'count_places':5,
    'count_available_places':5
    }
    """
    data = request.json
    new_parking = Parking(
        address=data["address"],
        opened=int(data["opened"]),
        count_places=data["count_places"],
        count_available_places=data["count_available_places"],
    )

    db.session.add(new_parking)
    db.session.commit()

    return jsonify(new_parking.to_json()), 201


@url_blueprint.route("/client_parking", methods=["POST"])
def reserve_parking():
    """
    Заезд на парковку

    Пример:
    {
    'client_id': 1,
    'parking_id': 1
    }
    """
    data = request.json
    check_parking = db.session.get(Parking, data["parking_id"])
    check_client = db.session.get(Client, data["client_id"])

    if check_client is None:
        return f"Клиент с id {data['client_id']} не найден", 404

    if check_parking is None:
        return f"Парковка с id {data['parking_id']} не найдена", 404

    if check_parking.opened is False:
        return "Парковка закрыта", 406

    if check_parking.count_available_places <= 0:
        return "На парковке нет мест", 406

    try:
        new_client_parking = ClientParking(
            time_in=datetime.now(),
            client_id=data["client_id"],
            parking_id=data["parking_id"],
        )
        check_parking.count_available_places -= 1
        db.session.add(new_client_parking)
        db.session.commit()

        return jsonify(new_client_parking.to_json()), 201

    except sqlalchemy.exc.IntegrityError:
        return (
            f"Клиент с id {data['client_id']} "
            f"уже припаркован на стоянке с id {data['parking_id']}", 406
        )


@url_blueprint.route("/client_parking", methods=["DELETE"])
def delete_parking():
    """
    Выезд с парковки

    Пример:
    {
    'client_id': 1,
    'parking_id': 1
    }
    """
    data = request.json
    parking = db.session.get(Parking, data["parking_id"])
    client = db.session.get(Client, data["client_id"])

    if parking is None:
        return f"Парковка с id {data['parking_id']} не найдена", 404

    if client is None:
        return f"Клиент с id {data['client_id']} не найден", 404

    client_parking_place = (
        db.session.query(ClientParking)
        .filter(
            ClientParking.client_id == data["client_id"],
            ClientParking.parking_id == data["parking_id"],
        )
        .first()
    )

    client_parking_place.time_out = datetime.now()
    parking.count_available_places += 1
    db.session.commit()

    if client.credit_card is None:
        return (f"Клиент расплатился наличными\n"
                f"{client_parking_place.to_json()}"), 201

    return jsonify(client_parking_place.to_json()), 201
