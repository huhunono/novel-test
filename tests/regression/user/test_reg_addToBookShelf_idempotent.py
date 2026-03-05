import pytest
import requests

from conftest import db_one
from tests.utils.assertions import assert_json_response,assert_ok_true

pytestmark = pytest.mark.regression


# ---------- Class B: Idempotency (State Control)  ----------
def test_reg_addToBookShelf_idempotent_should_not_duplicate(base_url, auth_http, db_conn, test_user_id):
    """
        Regression Test: Verify API Idempotency for Add-to-Bookshelf Operations.

        Logic Flow: addToBookShelf (First Call) → addToBookShelf (Duplicate Call) → listBookShelfByPage

        This test ensures state consistency and prevents redundant data entry:
        1. Idempotency Validation: Ensures identical requests do not create duplicate records.
        2. Business Logic Integrity: Verifies the backend handles "already exists" scenario gracefully.
        3. Collection Accuracy: Confirms the book count in the shelf remains <= 1, preventing UI display bugs.

    """
    """
    # 1) login -> auth session
    s = requests.Session()
    login_resp = s.post(base_url + "/user/login", data=test_user, timeout=20, allow_redirects=False)
    login_body = assert_json_response(login_resp)
    assert_ok_true(login_body)

    data=login_body.get("data")

    token = data.get("token")
    s.headers.update({"Authorization": token})
    
    target = str(book_id)
    """
    book_id = 2014580046711287808

    try:
        # 1) same book add twice
        r1 = auth_http.post(base_url + "/user/addToBookShelf", data={"bookId": book_id}, allow_redirects=False,timeout=10)
        b1 = assert_json_response(r1)
        assert_ok_true(b1)

        r2 = auth_http.post(base_url + "/user/addToBookShelf", data={"bookId": book_id}, allow_redirects=False,timeout=10)
        b2 = assert_json_response(r2)
        assert_ok_true(b2)

        # 2) verify no duplicates in shelf list
        # DB Validation
        row = db_one(
            db_conn,
            "SELECT COUNT(*) AS c FROM user_bookshelf WHERE user_id=%s AND book_id=%s",
            (test_user_id, book_id),
        )
        assert row and "c" in row, "DB query failed: check user_bookshelf(user_id, book_id)"
        assert row["c"] <= 1

    finally:
        try:
            resp = auth_http.delete(
                f"{base_url}/user/removeFromBookShelf/{book_id}",
                allow_redirects=False,
                timeout=10,
            )
            if resp.status_code != 200:
                print("cleanup failed:", resp.status_code, resp.text[:200])
        except Exception as e:
            print("cleanup exception:", repr(e))





