import pytest
from tests.utils.assertions import assert_json_response,assert_ok_true

@pytest.mark.reg_ci
def test_query_book_detail_basic(plain_http, base_url):
    """
        CI Regression Test: queryBookDetail basic sanity for PR gate.

        Logic Flow: queryBookDetail/{bookId} (GET)

        Checks:
        1) Data Fetching: Confirms the endpoint retrieves a specific book's metadata by ID.
        2) Identity Integrity: Verifies that the 'id' in the response matches the requested 'book_id'.
        3) Content Reliability: Ensures 'bookName' is a valid, non-empty string for frontend display.
    """
    book_id = 2010824442059300864
    resp=plain_http.get(base_url + f"/book/queryBookDetail/{book_id}",allow_redirects=False,timeout=20)
    body=assert_json_response(resp)
    assert_ok_true(body)
    data = body.get("data")
    assert isinstance(data, dict)

    assert str(data.get("id")) == str(book_id)

    book_name = data.get("bookName")
    assert isinstance(book_name, str)
    assert book_name.strip()




