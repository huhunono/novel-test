import requests
import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke


def test_login_success(base_url,plain_http,test_user):
    """
        Smoke Test: Verify Successful Authentication.

        This test ensures that the login credentials provided in the configuration
        are valid and the 'auth_http' fixture can successfully establish a session.
        It is a prerequisite for all subsequent authenticated API calls.
    """

    resp = plain_http.post(base_url +"/user/login", data=test_user, allow_redirects=False,timeout=10)
    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("data")is not None
