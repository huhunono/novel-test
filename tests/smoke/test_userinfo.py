import requests


def test_userinfo(auth_http,base_url):
    """
        Smoke Test: Verify retrieval of user profile with valid credentials.

        This test ensures that the Authorization header is correctly processed
        and the backend returns the personal profile data for the logged-in user.
    """

    headers={"Authorization":auth_http}
    resp=requests.get(base_url+"/user/userInfo",headers=headers,allow_redirects=False)

    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("content-type","")
    body=resp.json()
    assert body.get("ok") is True
    assert body.get("data")is not None


def test_userinfo_login_required(auth_http,base_url):
    """
        Smoke Test (Security): Verify that unauthorized access is blocked.

        Negative Test Case: Accessing the user info endpoint without an Authorization header.
        The system should gracefully deny access with a specific error code (1001).
    """
    resp = requests.get(base_url + "/user/userInfo",  allow_redirects=False)
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is False
    assert body["data"] is None
    assert body["code"] == 1001
