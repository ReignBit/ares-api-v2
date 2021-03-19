from datetime import datetime
from app.__main__ import API_ROOT

API_ROOT += "/users"

headers = {"Authorization": "Basic a2F0OnRlc3Q="}


def test_get_all_users(client):
    r = client.get(f"{API_ROOT}", headers=headers)
    assert r.status_code == 200
    assert type(r.json["data"]) is list


def test_valid_user(client):
    r = client.post(
        f"{API_ROOT}",
        json={"id": 0},
        headers=headers,
    )

    r = client.get(f"{API_ROOT}/0", headers=headers)
    assert r.status_code == 200
    assert r.json['data'] == [
        {
            "id": 0,
            "birthday": "None",
            "years": 0
        }
    ]


def test_get_user_invalid(client):
    r = client.get(f"{API_ROOT}/0", headers=headers)
    print(r.json)
    assert r.status_code == 404
    assert "No user with id `0`" in r.json["message"]


def test_create_user(client):
    r = client.post(
        f"{API_ROOT}",
        json={"id": 0},
        headers=headers,
    )
    assert r.status_code == 201
    assert "User added successfully" in r.json["message"]


def test_create_user_already_exists(client):
    r = client.post(
        f"{API_ROOT}",
        json={"id": 0},
        headers=headers,
    )
    assert r.status_code == 201

    r = client.post(
        f"{API_ROOT}",
        json={"id": 0},
        headers=headers,
    )

    assert r.status_code == 409
    assert r.json['message'] == "User `0` already exists!"


def test_delete_user(client):
    r = client.post(
        f"{API_ROOT}",
        json={"id": 1},
        headers=headers,
    )
    assert r.status_code == 201
    r = client.delete(f"{API_ROOT}/1", headers=headers)
    assert r.status_code == 200
    assert "Deleted user" in r.json["message"]


def test_patch_user(client):
    # creating user
    r = client.post(
        f"{API_ROOT}",
        json={"id": 1},
        headers=headers,
    )

    date_time_str = datetime.now()
    r = client.patch(
        f"{API_ROOT}/1",
        json={"birthday": date_time_str.strftime("%Y-%m-%d")},
        headers=headers
    )

    assert r.status_code == 200
    assert r.json['data'] == {
            "id": 1,
            "birthday": date_time_str.strftime("%Y-%m-%d"),
            "years": 0
        }
