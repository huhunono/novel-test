import requests


def test_userinfo(auth_http,base_url):

    headers={"Authorization":auth_http}
    resp=requests.get(base_url+"/user/userInfo",headers=headers,allow_redirects=False)

    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("content-type","")
    body=resp.json()
    assert body.get("ok") is True
    assert body.get("data")is not None


def test_userinfo_login_required(auth_http,base_url):
    resp = requests.get(base_url + "/user/userInfo",  allow_redirects=False)
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is False
    assert body["data"] is None
    assert body["code"] == 1001
