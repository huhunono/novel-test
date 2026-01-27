import pytest
from tests.utils.assertions import assert_ok_false

pytestmark = pytest.mark.regression


def test_reg_login_invalid_password_should_fail(base_url, plain_http):
    login_data = {
        "username": "13560421999",
        "password": "wrong_pw"
    }
    resp = plain_http.post(base_url + "/user/login", data=login_data, allow_redirects=False, timeout=10)

    assert resp.status_code < 500

    body = resp.json()
    assert_ok_false(body)
    assert body.get("code") != 200
