import requests
import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke
def test_list_rank(plain_http,base_url):
    """
        Smoke Test: Verify the Book Ranking List API.

        This test checks the system's ability to retrieve ranking data
        (e.g., 1 for Top Clicked, 2 forTop New Books) which is essential for the homepage.

    """
    param={"type":1}
    resp=plain_http.get(base_url+"/book/listRank",params=param,allow_redirects=False,timeout=10)
    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200
