import requests
def test_query_book_detail(base_url):
    """
        Smoke Test: Verify core availability of the Book Detail endpoint.

        This test ensures that a known valid book ID returns a successful
        response with the correct JSON structure. It serves as a health check
        for the primary business path.
    """

    book_id=2010824442059300864
    resp = requests.get(
        f"{base_url}/book/queryBookDetail/{book_id}", allow_redirects=False
    )
    # Assertion 1: Check HTTP Status Code
    assert resp.status_code == 200

    # Assertion 2: Strict Content-Type check with detailed error reporting.
    ct = resp.headers.get("content-type", "")
    if "application/json" not in ct:
        raise AssertionError(
            "Content type is not application/json.\n"f"url:{resp.request.url}\n"f"status:{resp.status_code}\n"
            f"ct:{ct}\n"
            f"text:{resp.text[:300]}\n")
    body = resp.json()


    # Assertion 3: Verify basic business success markers (Envelope Level)
    assert body.get("ok") is True
    assert body.get("code") == 200
    #data = body.get("data")
    #assert data is not None
    #id = data.get("id")
    #assert str(id) == str(book_id)




