import pytest
from tests.utils.assertions import assert_json_response,assert_ok_true,assert_ok_false


pytestmark = pytest.mark.regression


def test_reg_login_token_can_call_userinfo(auth_http, base_url):
    """
        Regression Test: Verify User Info retrieval using a valid Login Token.

        login → userInfo

        This test ensures the end-to-end authentication flow:
        1. Authorization headers are correctly propagated via auth_http.
        2. The backend correctly identifies the user session.
        3. The profile data structure remains consistent for UI consumption.
    """
    resp=auth_http.get(base_url+"/user/userInfo",allow_redirects=False,timeout=20)


    body = assert_json_response(resp)
    assert_ok_true(body)
    assert body.get("code") == 200

    #Data Integrity Validation
    data = body.get("data")
    assert data is not None
    assert isinstance(data, dict)

    #Critical Field Presence
    assert data.get("username") or data.get("nickName") or data.get("id")



def test_reg_userinfo_requires_auth(plain_http, base_url):
    resp = plain_http.get(base_url + "/user/userInfo", allow_redirects=False,timeout=20)

    assert resp.status_code in (200, 401, 403)

    if resp.status_code == 200:

        body = assert_json_response(resp)
        assert_ok_false(body)
        assert body.get("code") == 1001.

        assert body.get("data") is None






