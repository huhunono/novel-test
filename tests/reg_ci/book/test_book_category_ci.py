import pytest
from tests.utils.assertions import assert_json_response,assert_ok_true

@pytest.mark.reg_ci
def test_reg_ci_list_book_category_min_contract(plain_http, base_url):
    """
        CI Regression Test: listBookCategory basic sanity for PR gate.

        Logic Flow: listBookCategory (GET)

        Checks:
        1) Application success: ok=true and code=200
        2) Data shape: 'data' is a non-empty list
        3) Minimal item sanity: first item has 'id' and non-empty 'name'
    """
    resp = plain_http.get(base_url + "/book/listBookCategory", allow_redirects=False, timeout=20)
    body=assert_json_response(resp)
    assert_ok_true(body)
    assert body.get("code") == 200
    data = body.get("data")
    assert isinstance(data, list)
    assert len(data) > 0

    # first item
    first = data[0]
    assert isinstance(first, dict)

    assert first.get("id") is not None
    assert isinstance(first.get("name"), str)
    assert first.get("name").strip()






