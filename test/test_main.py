from fastapi.testclient import TestClient
from main import api, tickets

client = TestClient(api)

def clear_tickets():
    tickets.clear()


def test_home():
    clear_tickets()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}


def test_create_ticket():
    clear_tickets()
    response = client.post("/ticket", json={
        "id": 1,
        "flight_name": "Flight A",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Paris"
    })
    assert response.status_code == 200
    assert response.json()["flight_name"] == "Flight A"


def test_get_tickets():
    clear_tickets()
    client.post("/ticket", json={
        "id": 1,
        "flight_name": "Flight A",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Paris"
    })
    response = client.get("/ticket")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_update_ticket():
    clear_tickets()
    client.post("/ticket", json={
        "id": 1,
        "flight_name": "Flight A",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Paris"
    })

    response = client.put("/ticket/1", json={
        "id": 1,
        "flight_name": "Flight ABC",
        "flight_date": "2025-10-16",
        "flight_time": "16:00",
        "destination": "London"
    })
    assert response.status_code == 200
    assert response.json()["flight_name"] == "Flight B"


def test_delete_ticket():
    clear_tickets()
    client.post("/ticket", json={
        "id": 1,
        "flight_name": "Flight B",
        "flight_date": "2025-10-16",
        "flight_time": "16:00",
        "destination": "London"
    })

    response = client.delete("/ticket/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert len(tickets) == 0
