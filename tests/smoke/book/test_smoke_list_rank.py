import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke
def test_list_rank(book_client):
    """
        Smoke Test: Verify the Book Ranking List API.

        This test checks the system's ability to retrieve ranking data
        (e.g., 1 for Top Clicked, 2 forTop New Books) which is essential for the homepage.

    """
    resp = book_client.list_rank(type_=1, allow_redirects=False, timeout=10)
    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200
