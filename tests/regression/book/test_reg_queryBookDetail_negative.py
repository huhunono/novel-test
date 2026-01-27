import pytest
import requests
from tests.utils.assertions import assert_json_response,assert_ok_false

pytestmark = pytest.mark.regression

# ---------- Class B: Valid format but NON-existent ----------
@pytest.mark.xfail(reason="Known issue: endpoint returns HTML 404 page instead of JSON on not-found")
def test_reg_queryBookDetail_nonexistent_bookId_should_fail(base_url,plain_http):
    """

        Regression Test: Verify System Graceful Failure for Non-existent Resources.

        Logic Flow: queryBookDetail/{nonExistentId} (e.g., 999999999999)

    """
    # valid-format but non-existent bookId
    book_id = 999999999999

    resp = plain_http.get(f"{base_url}/book/queryBookDetail/{book_id}", allow_redirects=False, timeout=10 )
    # not server error
    assert resp.status_code < 500

    if resp.status_code == 200:
        body=assert_json_response(resp)
        assert_ok_false(body)

# ---------- Class C: Invalid format ----------
@pytest.mark.xfail(reason="Known issue: API returns HTML 404 page instead of JSON on error path")
@pytest.mark.parametrize("invalid_book_id", [-1, "abc"])
def test_reg_queryBookDetail_invalid_bookId_should_be_rejected( base_url, invalid_book_id):

    """

        Regression Test: Verify Input Validation and Rejection for Malformed Data.

        Logic Flow: queryBookDetail/{invalid_id} (Parametrized with -1, "abc")

    """
    resp = requests.get(
        f"{base_url}/book/queryBookDetail/{invalid_book_id}",allow_redirects=False,timeout=10)
    assert resp.status_code < 500

    if resp.status_code == 200:
        body=assert_json_response(resp)
        assert_ok_false(body)