import requests


def test_list_book_category_smoke(base_url):
    resp=requests.get(base_url+"/book/listBookCategory",allow_redirects=False)

    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")

    body = resp.json()
    assert body.get("ok") is True
    assert body.get("code") == 200
