import os

import pytest
import requests
import pymysql


@pytest.fixture(scope="session")
def http():
    return requests.Session()


@pytest.fixture(scope="session")
def auth_token(base_url):
    resp = requests.post(
        base_url + "/user/login",
        #Form parsing
        data={
            "username": "13560421999",
            "password": "123456"
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
    assert body.get("ok") is True, body
    token = body["data"]["token"]
    assert isinstance(token, str) and token, body
    return token


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "http://172.28.0.1:8083")

@pytest.fixture()
def auth_http(auth_token):
    s = requests.Session()
    s.headers.update({
        "Authorization": auth_token
    })
    yield s
    s.close()

@pytest.fixture()
def plain_http():
    s=requests.Session()
    yield s
    s.close()


@pytest.fixture(scope="session")
def test_user():
    return {"username": "13560421999", "password": "123456"}


@pytest.fixture(scope="session")
def db_conn():
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "novel"),
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
    yield conn
    conn.close()

def db_one(conn, sql, params=None):
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()

def db_all(conn, sql, params=None):
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchall()


@pytest.fixture(scope="session")
def test_user_id(db_conn, test_user):
    username = test_user["username"]
    row = db_one(db_conn, "SELECT id FROM user WHERE username=%s", (username,))
    assert row and "id" in row, f"user not found in DB: username={username}"
    return row["id"]