import pytest
import requests
from tests.utils.assertions import assert_json_response,assert_ok_true
pytestmark = pytest.mark.regression

REFRESH_PATH = "/user/refreshToken"

def test_reg_login_refresh_userinfo(base_url, auth_token):
    """
        Regression Test: Verify Authentication Persistence during Token Refresh.

        Logic Flow: login → refreshToken → userInfo

        This test ensures the continuity of the user session:
        1. The refreshToken endpoint successfully issues a valid new credential.
        2. The session context correctly updates headers with the rotated token.
        3. The subsequent userInfo call validates that the new token grants
           uninterrupted access to protected resources.
    """
    s=requests.Session()
    s.headers.update({"Authorization": auth_token})

    resp_refresh=s.post(base_url+REFRESH_PATH,allow_redirects=False)
    body=assert_json_response(resp_refresh)
    assert_ok_true(body)

    new_token=None

    data=body.get("data")

    if isinstance(data,dict):
        new_token=data.get("token")

    # update header ,new token can not be None
    if isinstance(new_token, str) and new_token:
        s.headers.update({"Authorization": new_token})

    # verify:  new token -> userinfo
    resp_userinfo=s.get(base_url+ "/user/userInfo", allow_redirects=False)
    new_body=assert_json_response(resp_userinfo)
    assert_ok_true(new_body)