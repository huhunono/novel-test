import pytest
from tests.utils.assertions import assert_json_response,assert_ok_true


@pytest.mark.reg_ci

def test_query_index_list_basic(plain_http, base_url):
    """
        CI Regression Test: queryIndexList basic sanity for PR gate.

        Logic Flow: queryIndexList?bookId={bookId} (GET)

        Checks:
        1) Service Availability: Confirms the chapter index service is reachable and returns 200 OK.
        2) Response Structure: Validates 'data' object contains a 'list' of chapter entries.
        3) Content Integrity: Ensures chapters exist (len > 0) and each has a valid 'id' and 'indexName'.

    """
    book_id = 2010824442059300864
    resp=plain_http.get(base_url + "/book/queryIndexList",params={"bookId":book_id},allow_redirects=False,timeout=20)
    body = assert_json_response(resp)
    assert_ok_true(body)
    assert body.get("code") == 200

    data = body.get("data")
    assert data is not None
    assert isinstance(data, dict)

    index_list = data.get("list")
    assert isinstance(index_list, list)

    assert len(index_list) > 0

    first = index_list[0]
    assert isinstance(first, dict)

    index_id = first.get("id")
    assert index_id is not None

    index_name = first.get("indexName")
    assert isinstance(index_name, str)
    assert index_name.strip()

