from app.__main__ import API_ROOT

headers = {"Authorization": "Basic dGVzdDp0ZXN0"}


def create_guild_and_user(client):
    client.post(
        f"{API_ROOT}/guilds",
        json={"id": 0},
        headers=headers,
    )
    client.post(f"{API_ROOT}/users", json={"id": 0}, headers=headers)


def test_get_all_members(client):
    # Create users
    client.post(
        f"{API_ROOT}/users",
        json={"id": 0},
        headers=headers,
    )
    client.post(
        f"{API_ROOT}/users",
        json={"id": 0},
        headers=headers,
    )
    # Create members
    client.post(
        f"{API_ROOT}/guilds/0/members",
        json={"id": 0},
        headers=headers,
    )

    client.post(
        f"{API_ROOT}/guilds/0/members",
        json={"id": 1},
        headers=headers,
    )
    # test
    r = client.get(f"{API_ROOT}/guilds/0/members", headers=headers)
    assert r.status_code == 200
    print(r.json['data'])
    assert r.json['data'] == [
        {
            "gid": 0,
            "id": 0,
            "xp": 1,
            "level": 1,
            "settings": None
        },
        {
            "gid": 0,
            "id": 1,
            "xp": 1,
            "level": 1,
            "settings": None
        }
    ]


def test_get_members_invalid(client):
    create_guild_and_user(client)

    r = client.get(f"{API_ROOT}/guilds/0/0", headers=headers)
    assert r.status_code == 404
    assert "No member with id `0`" in r.json["message"]


def test_create_members(client):
    create_guild_and_user(client)

    r = client.post(
        f"{API_ROOT}/guilds/0/members",
        json={"id": 0},
        headers=headers,
    )
    assert r.status_code == 201
    assert "Member added successfully" in r.json["message"]


def test_delete_member(client):
    create_guild_and_user(client)

    r = client.post(
        f"{API_ROOT}/guilds/0/members",
        json={"id": 0},
        headers=headers,
    )
    print(r.status_code)
    print(r.json)
    r = client.delete(f"{API_ROOT}/guilds/0/0", headers=headers)
    assert r.status_code == 200
    assert "Deleted member" in r.json["message"]


def test_delete_member_invalid(client):
    r = client.delete(f"{API_ROOT}/guilds/0/0", headers=headers)
    assert r.status_code == 404


def test_patch_member_data(client):
    create_guild_and_user(client)
    r = client.post(
        f"{API_ROOT}/guilds/0/members",
        json={"id": 0},
        headers=headers,
    )

    json_data = {"settings": {"test": 1}}

    r = client.patch(f"{API_ROOT}/guilds/0/0", json=json_data, headers=headers)

    assert r.status_code == 200
    print(r.json)
    assert r.json["data"]["settings"]["test"] == 1
