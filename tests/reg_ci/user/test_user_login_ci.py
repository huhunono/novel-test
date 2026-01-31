import pytest
import requests

from tests.utils.assertions import assert_json_response,assert_ok_true
@pytest.mark.reg_ci
def test_reg_ci_login_and_token_usable(plain_http, base_url,test_user):
    """
        CI Regression Test: Authentication Flow and Token Usability.

        Logic Flow: /user/login (POST) -> /user/userInfo (GET with Header)

        Checks:
        1) Authentication: Verifies that valid credentials yield a 200 OK and a non-empty token.
        2) Authorization Bridge: Confirms the generated token can be successfully injected into subsequent headers.
        3) Identity Persistence: Validates that the 'userInfo' retrieved via the token correctly matches the logged-in user.

    """

    resp = plain_http.post(base_url + "/user/login",data=test_user,allow_redirects=False,timeout=20)
    body=assert_json_response(resp)
    assert_ok_true(body)
    assert body.get("code") == 200

    data=body.get("data")
    assert isinstance(data,dict)

    token=data.get("token")
    assert isinstance(token, str)
    assert token.strip()

    # use token to access protected API
    auth_http = requests.Session()
    auth_http.headers.update({"Authorization": token})

    resp_userinfo = auth_http.get(base_url + "/user/userInfo",allow_redirects=False,timeout=20)
    body_userinfo = assert_json_response(resp_userinfo)
    assert_ok_true(body_userinfo)
    assert body_userinfo.get("code") == 200
    user_data = body_userinfo.get("data")
    assert isinstance(user_data, dict)
    assert user_data.get("username")==test_user.get("username")