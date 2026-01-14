import requests
def test_query_book_detail(base_url):
    book_id=2010824442059300864
    resp = requests.get(
        f"{base_url}/book/queryBookDetail/{book_id}", allow_redirects=False
    )
    assert resp.status_code == 200
    ct = resp.headers.get("content-type", "")
    if "application/json" not in ct:
        raise AssertionError(
            "Content type is not application/json.\n"f"url:{resp.request.url}\n"f"status:{resp.status_code}\n"
            f"ct:{ct}\n"
            f"text:{resp.text[:300]}\n")
    body = resp.json()
    #assert body.get("msg") == "SUCCESS"
    assert body.get("ok") is True
    assert body.get("code") == 200
    #data = body.get("data")
    #assert data is not None
    #id = data.get("id")
    #assert str(id) == str(book_id)




