import pytest
from tests.utils.assertions import assert_json_response,assert_ok_true

pytestmark = pytest.mark.regression


# ---------- Class B: Idempotency (State Control)  ----------
def test_reg_addToBookShelf_idempotent_should_not_duplicate(base_url, auth_http):
    """
        Regression Test: Verify API Idempotency for Add-to-Bookshelf Operations.

        Logic Flow: addToBookShelf (First Call) → addToBookShelf (Duplicate Call) → listBookShelfByPage

        This test ensures state consistency and prevents redundant data entry:
        1. Idempotency Validation: Ensures identical requests do not create duplicate records.
        2. Business Logic Integrity: Verifies the backend handles "already exists" scenario gracefully.
        3. Collection Accuracy: Confirms the book count in the shelf remains <= 1, preventing UI display bugs.
    """
    book_id = 2010824442059300864
    target = str(book_id)

    # 1) same book add twice
    r1 = auth_http.post(base_url + "/user/addToBookShelf", data={"bookId": book_id}, allow_redirects=False,timeout=10)
    b1 = assert_json_response(r1)
    assert_ok_true(b1)

    r2 = auth_http.post(base_url + "/user/addToBookShelf", data={"bookId": book_id}, allow_redirects=False,timeout=10)
    b2 = assert_json_response(r2)
    assert_ok_true(b2)

    # 2) verify no duplicates in shelf list
    r3 = auth_http.get(base_url + "/user/listBookShelfByPage",params={"pageNum": 1, "pageSize": 200},allow_redirects=False,timeout=10)
    b3 = assert_json_response(r3)
    assert_ok_true(b3)

    items=b3.get("data").get("list")
    count=0
    for x in items:
        id=str(x.get("bookId"))
        if id==target:
            count=count+1
    assert count <=1





