import requests
import pytest

pytestmark = pytest.mark.smoke


def test_login_success(base_url):
    """
        Smoke Test: Verify Successful Authentication.

        This test ensures that the login credentials provided in the configuration
        are valid and the 'auth_http' fixture can successfully establish a session.
        It is a prerequisite for all subsequent authenticated API calls.
    """
    login_data={
        "username": "13560421999",
        "password": "123456"
    }
    resp = requests.post(base_url +"/user/login", data=login_data, allow_redirects=False)
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("content-type","")
    body=resp.json()
    assert body.get("ok") is True
    assert body.get("data")is not None
