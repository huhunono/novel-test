import requests
import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke

def test_list_book_category_smoke(plain_http,base_url):
    """
        Smoke Test: Verify the Book Category Lookup API.

        This interface provides the fundamental category list (e.g., Fantasy, Romance)
        used across the entire site. Failure here typically impacts navigation and search.
    """
    resp=plain_http.get(base_url+"/book/listBookCategory",allow_redirects=False,timeout=10)

    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200

