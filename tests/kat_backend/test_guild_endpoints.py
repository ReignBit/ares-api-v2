from app.__main__ import API_ROOT

API_ROOT += "/guilds"

headers = {"Authorization": "Basic dGVzdDp0ZXN0"}


def test_get_all_guilds(client):
    r = client.get(f"{API_ROOT}", headers=headers)
    assert r.status_code == 200
    assert r.json["data"] == []


def test_get_valid_guild(client):
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
            "settings": {}
        }
    ]


def test_post_already_exists(client):
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
    assert r.json["message"] == "Guild `0` already exists!"


def test_get_guilds_invalid(client):
    r = client.get(f"{API_ROOT}/0", headers=headers)
    print(r.json)
    assert r.status_code == 404
    assert "No guild with id `0`" in r.json["message"]


def test_create_guilds(client):
    r = client.post(
        f"{API_ROOT}",
        json={"id": 0},
        headers=headers,
    )
    assert r.status_code == 201
    assert "Guild added successfully" in r.json["message"]


def test_delete_guild(client):
    r = client.post(
        f"{API_ROOT}",
        json={"id": 1},
        headers=headers,
    )
    assert r.status_code == 201
    r = client.delete(f"{API_ROOT}/1", headers=headers)
    assert r.status_code == 200
    assert "Deleted guild" in r.json["message"]


def test_delete_guild_invalid(client):
    r = client.delete(f"{API_ROOT}/0", headers=headers)
    assert r.status_code == 404


def test_patch_guild_settings(client):
    client.post(f"{API_ROOT}", json={"id": 0}, headers=headers)
    test_data = {"settings": {"settings": {"prefix": "£"}, "test": 1}}

    r = client.patch(f"{API_ROOT}/0", json=test_data, headers=headers)

    assert r.status_code == 200
    print(r.json)
    assert r.json["data"]["settings"]["test"] == 1
