"""
Модуль с тестами
"""

import time

import pytest


def test_app_config(app):
    """Конфиг тестов"""
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_route_status(client, route):
    """Тест для проверки статус кода ответа маршрутов"""
    rv = client.get(route)
    assert rv.status_code == 200


def test_create_client(client) -> None:
    """Тест создания клиента"""
    client_data = {
        "name": "name",
        "surname": "surname",
        "credit_card": "credit_card",
        "car_number": "car_number",
    }
    resp = client.post("/clients", json=client_data)
    assert resp.status_code == 201


def test_create_parking(client) -> None:
    """Тест создания парковки"""
    client_data = {
        "address": "address",
        "opened": "1",
        "count_places": 5,
        "count_available_places": 5,
    }
    resp = client.post("/parking", json=client_data)
    assert resp.status_code == 201


@pytest.mark.parking
def test_enter_parking(client) -> None:
    """Тест заезда на парковку"""
    client_data = {"client_id": 2, "parking_id": 1}
    resp = client.post("/client_parking", json=client_data)
    assert resp.status_code == 201


@pytest.mark.parking
def test_leave_parking(client) -> None:
    """Тест выезда на парковку"""
    client_data = {"client_id": 1, "parking_id": 1}
    resp = client.delete("/client_parking", json=client_data)
    assert resp.status_code == 201


def test_parking_is_closed(client) -> None:
    """Тест парковка закрыта"""
    client_data = {"client_id": 1, "parking_id": 2}
    resp = client.post("/client_parking", json=client_data)
    assert "Парковка закрыта" in resp.text


def test_parking_no_slots(client) -> None:
    """Тест на парковке нет места"""
    client_data = {"client_id": 1, "parking_id": 3}
    resp = client.post("/client_parking", json=client_data)
    assert "На парковке нет мест" in resp.text


def test_parking_slots_minus(client) -> None:
    """Тест на парковке уменьшается свободное место"""
    client_data = {"client_id": 2, "parking_id": 1}
    client.post("/client_parking", json=client_data)
    parking = client.get("/parking/1", json=client_data)
    data = parking.json
    assert data["count_available_places"] == 4


def test_parking_slots_plus(client) -> None:
    """Тест на парковке увеличивается свободное место"""
    client_data = {"client_id": 1, "parking_id": 1}
    client.delete("/client_parking", json=client_data)
    parking = client.get("/parking/1", json=client_data)
    data = parking.json
    assert data["count_available_places"] == 6


def test_time_in_out(client) -> None:
    """Тест время выезда больше времени заезда"""
    client_data = {"client_id": 2, "parking_id": 1}
    client.post("/client_parking", json=client_data)
    time.sleep(1)

    resp_out = client.delete("/client_parking", json=client_data)
    assert resp_out.json["time_in"] < resp_out.json["time_out"]


def test_no_credit_card(client) -> None:
    """Тест нет кредитной карты"""
    client_data = {"client_id": 3, "parking_id": 1}
    resp = client.delete("/client_parking", json=client_data)
    assert "Клиент расплатился наличными" in resp.text
    assert resp.status_code == 201


def test_parking_not_exist_leave(client) -> None:
    """Тест выезд с несуществующей парковки"""
    client_data = {"client_id": 1, "parking_id": 5}
    resp = client.delete("/client_parking", json=client_data)
    assert f"Парковка с id {client_data['parking_id']} не найдена" in resp.text


def test_client_parking_twice(client) -> None:
    """Тест клиент паркуется дважды на 1 стоянке"""
    client_data = {"client_id": 3, "parking_id": 1}
    resp = client.post("/client_parking", json=client_data)
    assert (
        f"Клиент с id {client_data['client_id']} "
        f"уже припаркован на стоянке с id {client_data['parking_id']}" in resp.text
    )
    assert resp.status_code == 406
    assert resp.status_code != 400
