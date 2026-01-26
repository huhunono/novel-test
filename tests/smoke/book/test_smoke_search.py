import requests
import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke
def test_search_by_page(base_url,plain_http):
    """
        Smoke Test: Verify the Book Search & Pagination API.

        This test validates the core search functionality which involves keyword matching
        and database pagination logic. It ensures users can find content via the
        global search bar.
    """
    param={"curr":1,"limit":20,"keyword":"roman"}
    resp = plain_http.get(base_url + "/book/searchByPage",params=param, allow_redirects=False,timeout=10)
    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200







