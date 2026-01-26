import requests
import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke

def test_index_news(base_url,plain_http):
    """
        Smoke Test: Verify the Index News API is reachable and returns a valid response.

        This test ensures that the core news service is functional without performing
        deep data validation.
    """
    resp=plain_http.get(base_url+"/news/listIndexNews",timeout=10)

    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200
