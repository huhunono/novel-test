import logging
import os
from typing import Dict, Generator, Optional, Sequence

import pymysql
import pymysql.connections
import pymysql.cursors
import pytest

from clients.base_client import BaseClient
from clients.book_client import BookClient
from clients.news_client import NewsClient
from clients.user_client import UserClient
from tests.data.users import TEST_PASSWORD, TEST_USERNAME
from tests.utils.db_helpers import db_one

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def auth_token(base_url: str) -> str:
    client = BaseClient(base_url=base_url)
    resp = client.post(
        "/user/login",
        data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        },
        allow_redirects=False,
    )
    logger.debug("LOGIN status=%s ct=%s body=%s",
                 resp.status_code,
                 resp.headers.get("Content-Type"),
                 resp.text[:500])

    ct = resp.headers.get("Content-Type", "")
    assert resp.status_code == 200
    assert "application/json" in ct, (
        f"Login response not JSON. "
        f"status={resp.status_code}, ct={ct}, text={resp.text[:200]}"
    )
    body = resp.json()
    assert body.get("ok") is True, body
    token: str = body["data"]["token"]
    assert isinstance(token, str) and token, body
    client.close()
    return token


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://172.28.0.1:8083")


@pytest.fixture()
def auth_http(auth_token: str, base_url: str) -> Generator[BaseClient, None, None]:
    client = BaseClient(
        base_url=base_url,
        default_headers={"Authorization": auth_token},
    )
    try:
        yield client
    finally:
        client.close()


@pytest.fixture()
def plain_http(base_url: str) -> Generator[BaseClient, None, None]:
    client = BaseClient(base_url=base_url)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture()
def news_client(plain_http: BaseClient) -> NewsClient:
    """NewsClient wrapping the plain HTTP client (no auth required for listIndexNews)."""
    return NewsClient(plain_http)


@pytest.fixture()
def book_client(plain_http: BaseClient) -> BookClient:
    """BookClient wrapping the plain HTTP client (no auth — read-only endpoints)."""
    return BookClient(plain_http)


@pytest.fixture()
def auth_book_client(auth_http: BaseClient) -> BookClient:
    """BookClient wrapping the authenticated HTTP client (write endpoints: addBookComment etc)."""
    return BookClient(auth_http)


@pytest.fixture()
def user_client(auth_http: BaseClient) -> UserClient:
    """UserClient wrapping the authenticated HTTP client."""
    return UserClient(auth_http)


@pytest.fixture(scope="session")
def test_user() -> Dict[str, str]:
    return {"username": TEST_USERNAME, "password": TEST_PASSWORD}


@pytest.fixture(scope="session")
def db_conn() -> Generator[pymysql.connections.Connection, None, None]:
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "password"),
        database=os.getenv("DB_NAME", "novel_plus"),
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture(scope="session")
def test_user_id(
    db_conn: pymysql.connections.Connection,
    test_user: Dict[str, str],
) -> int:
    username: str = test_user["username"]
    row = db_one(db_conn, "SELECT id FROM user WHERE username=%s", (username,))
    assert row and "id" in row, f"user not found in DB: username={username}"
    return row["id"]
