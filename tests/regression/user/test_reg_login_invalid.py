import pytest
from tests.utils.assertions import assert_ok_false

pytestmark = pytest.mark.regression


def test_reg_login_invalid_password_should_fail(base_url, plain_http,test_user):
    """
        CI Regression Test: Handle Login with invalid credentials.

        Logic Flow: /user/login (POST) with incorrect password

        Checks:
        1) Service Resilience: Confirms the server does not crash (HTTP < 500) on invalid input.
        2) Error Handling: Validates that 'ok' is false and the business 'code' is not 200.
        3) Security: Ensures that incorrect passwords do not grant access to the system.

    """
    login_data = {
        "username": "13560421999",
        "password": "wrong_pw"
    }
    resp = plain_http.post(base_url + "/user/login", data=login_data, allow_redirects=False, timeout=10)

    assert resp.status_code < 500

    body = resp.json()
    assert_ok_false(body)
    assert body.get("code") != 200
