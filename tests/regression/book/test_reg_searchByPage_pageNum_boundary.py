import pytest

pytestmark = pytest.mark.regression

# ---------------------- BVA 1: pageNum = 0 ----------------------
@pytest.mark.xfail(reason="Known issue: pageNum=0 accepted as valid")
def test_reg_pageNum_zero_should_be_rejected_or_safely_handled(base_url, plain_http):
    """
        Regression Test: Verify Boundary Handling for Invalid Page Index (Zero).

        Logic Flow: searchByPage?curr=0

        This test ensures the system handles out-of-bounds pagination gracefully:
        1. Robustness: Prevents 500 Internal Server Errors when the page index is 0.
        2. Auto-correction vs. Rejection: If the API returns 200, it MUST correct the pageNum to 1.
           Otherwise, it should return a business-level error (ok=false).
        3. Bug Detection: Catching cases where pageNum=0 is reflected back in the response, which is logically invalid.
    """
    params = {"curr":"0"}
    resp =plain_http.get(base_url + "/book/searchByPage", params=params, allow_redirects=False,timeout=10)

    assert resp.status_code < 500

    if resp.status_code != 200:
        return

    body = resp.json()
    assert isinstance(body, dict)
    # If API returns success, it must correct pageNum to >=1
    if body.get("ok") is True and body.get("code") == 200:
        page_num = int(str(body["data"].get("pageNum")))
        assert page_num >= 1, f"Expected pageNum corrected to >=1, got {page_num} (BUG)"
    else:
        # business rejection is also acceptable
        assert body.get("ok") is False or body.get("code") != 200

# ---------------------- BVA 2: pageNum = 2 (Empty Page) ----------------------
def test_reg_pageNum_two_should_return_empty_or_valid_result(base_url, plain_http):
    """
        Regression Test: Verify Pagination Behavior on Valid Out-of-Range Requests.

        Logic Flow: searchByPage?curr=2 (Assuming total data < 2 pages)

        This test ensures the API follows standard pagination conventions:
        1. Consistency: A request for an empty page should still be a "success" (200 OK) but return an empty list.
        2. Metadata Integrity: Verifies that even if the list is empty, the response structure and page metadata remain intact.
        3. Data Type Safety: Ensures 'list' field is an empty list [] rather than null or missing.
     """
    params = {"curr":"2"}
    resp =plain_http.get(base_url + "/book/searchByPage", params=params, allow_redirects=False,timeout=10)

    assert resp.status_code < 500
    body = resp.json()
    assert isinstance(body, dict)

    assert body.get("ok") is True
    assert body.get("code") == 200

    data = body.get("data")
    assert isinstance(data, dict)

    assert int(str(data.get("pageNum"))) == 2
    assert isinstance(data.get("list"), list)
    assert len(data["list"]) == 0
    assert int(str(data.get("pages"))) >= 1