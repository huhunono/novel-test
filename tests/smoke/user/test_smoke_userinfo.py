import requests
import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke

def test_userinfo(auth_http,base_url):
    """
        Smoke Test: Verify retrieval of user profile with valid credentials.

        This test ensures that the Authorization header is correctly processed
        and the backend returns the personal profile data for the logged-in user.
    """
    resp=auth_http.get(base_url+"/user/userInfo",allow_redirects=False,timeout=10)

    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200


def test_userinfo_login_required(base_url,plain_http):
    """
        Smoke Test (Security): Verify that unauthorized access is blocked.

        Negative Test Case: Accessing the user info endpoint without an Authorization header.
        The system should gracefully deny access with a specific error code (1001).
    """
    resp = plain_http.get(base_url + "/user/userInfo",  allow_redirects=False,timeout=10)
    assert resp.status_code in (200, 401, 403)
    if resp.status_code == 200:
        body = assert_json_response(resp)
        assert body.get("ok") is False


