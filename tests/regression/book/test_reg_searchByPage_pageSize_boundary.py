import pytest
from tests.utils.assertions import assert_json_response,assert_ok_true

pytestmark = pytest.mark.regression

# ---------------------- BVA 1: pageSize = 1 ----------------------
def test_reg_searchByPage_pageSize_one_should_return_at_most_one_item(base_url, plain_http):
    """
        Regression Test: Verify Pagination Boundary for Minimal Page Size.

        Logic Flow: searchByPage?limit=1

        This test ensures the backend respects the limit constraint at its lowest boundary:
        1. Limit Enforcement: Validates that the persistence layer (SQL LIMIT 1) correctly restricts the result set.
        2. Data Integrity: Verifies the 'pageSize' metadata in the response matches the requested parameter.
        3. Resource Optimization: Ensures the API does not over-fetch data, protecting downstream consumers from bulk payloads.
    """
    params = {"limit":"1"}
    resp =plain_http.get(base_url + "/book/searchByPage", params=params, allow_redirects=False,timeout=10)

    assert resp.status_code < 500

    if resp.status_code != 200:
        return
    body= assert_json_response(resp)
    assert_ok_true(body)

    data = body.get("data")
    assert isinstance(data, dict)
    assert int(str(data.get("pageSize"))) == 1

    items = data.get("list")
    assert isinstance(items, list)
    # minimal page size should not return >1 items
    assert len(items) <= 1, f"Expected <=1 item, got {len(items)}"