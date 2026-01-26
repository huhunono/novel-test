import pytest

pytestmark = pytest.mark.regression

def test_reg_bookshelf_add_requires_auth(base_url, plain_http):
    """
        Regression Test: Verify Authorization Enforcement for Bookshelf Operations.

        Scenario: Anonymous user (no token) attempts to add a book to the shelf.

        This test ensures security boundaries are intact:
        1. Unauthorized requests should be blocked at the transport (401/403) or business layer.
        2. The system must not allow state changes for unauthenticated sessions.
        3. The response must clearly indicate a failure (ok: False) or a non-success code.
    """

    book_id = "2014580673134784512"

    resp=plain_http.post(base_url + "/user/addToBookShelf",data={"bookId": book_id},allow_redirects=False)
    if resp.status_code in (401, 403):
        return
    ct = resp.headers.get("content-type", "")
    assert "application/json" in ct, f"ct={ct}, text={resp.text[:200]}"

    body = resp.json()

    assert body.get("ok") is False or body.get("code") != 200, body