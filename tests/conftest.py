import pytest
import requests


@pytest.fixture
def auth_http():
    base_url = "http://172.28.0.1:8083"
    session = requests.Session()

    resp = session.post(
        base_url + "/user/login",
        #Form parsing
        data={
            "username": "13560421999",
            "password": "123456"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        allow_redirects=False,
    )
    print("\n===== DEBUG LOGIN RESPONSE =====")
    print("Status Code:", resp.status_code)
    print("Content-Type:", resp.headers.get("Content-Type"))
    print("Headers:", dict(resp.headers))
    print("Raw Text:", resp.text[:500])
    print("================================\n")

    ct = resp.headers.get("Content-Type", "")
    assert resp.status_code == 200
    assert "application/json" in ct, (
        f"Login response not JSON. "
        f"status={resp.status_code}, ct={ct}, text={resp.text[:200]}"
    )

    body = resp.json()
    assert body.get("ok") is True

    return body["data"]["token"]


@pytest.fixture(scope="session")
def base_url():
    return "http://172.28.0.1:8083"