import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke
def test_search_by_page(book_client):
    """
        Smoke Test: Verify the Book Search & Pagination API.

        This test validates the core search functionality which involves keyword matching
        and database pagination logic. It ensures users can find content via the
        global search bar.
    """
    resp = book_client.search_by_page(
        page_num=1, page_size=20,
        extra_params={"keyword": "roman"},
        allow_redirects=False, timeout=10,
    )
    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200
    assert body.get("data") is not None, f"data is null: {body}"







