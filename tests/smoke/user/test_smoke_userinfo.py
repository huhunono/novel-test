import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke


def test_userinfo(user_client):
    """
        Smoke Test: Verify retrieval of user profile with valid credentials.

        This test ensures that the Authorization header is correctly processed
        and the backend returns the personal profile data for the logged-in user.
    """
    resp = user_client.user_info(allow_redirects=False, timeout=10)

    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200


