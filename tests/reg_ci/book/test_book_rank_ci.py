import pytest
from tests.utils.assertions import assert_json_response,assert_ok_true

@pytest.mark.reg_ci
def test_list_rank_type_1_basic(book_client):
    """
        CI Regression Test: listRank (Type 1) basic sanity for PR gate.

        Logic Flow: listRank?type=1 (GET)

        Checks:
        1) Application success: ok=true and HTTP-level JSON integrity.
        2) Data shape: 'data' returns a list containing multiple ranking entries (len > 1).
        3) Minimal item sanity: Each entry must link to a category (catId) and specific ID,
           with a valid 'bookName' string for display.

    """
    resp = book_client.list_rank(type_=1, allow_redirects=False, timeout=20)
    body=assert_json_response(resp)
    assert_ok_true(body)

    data = body.get("data")
    assert isinstance(data, list)

    assert len(data)>1
    first = data[0]
    assert isinstance(first, dict)
    assert first.get("catId") is not None
    assert first.get("id") is not None
    assert isinstance(first.get("bookName"), str)




