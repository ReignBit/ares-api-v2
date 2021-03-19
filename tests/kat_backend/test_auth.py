from app.__main__ import API_ROOT


def test_unauthorized(client):
    r = client.get(
        f"{API_ROOT}/guilds", headers={"Authorization": "Basic incorrect"}
    )

    assert r.status_code == 403


def test_no_auth(client):
    r = client.get(f"{API_ROOT}/guilds")
    print(r)
    assert r.status_code == 403
