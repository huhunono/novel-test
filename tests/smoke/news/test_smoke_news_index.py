import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke

def test_index_news(news_client):
    """
        Smoke Test: Verify the Index News API is reachable and returns a valid response.

        This test ensures that the core news service is functional without performing
        deep data validation.
    """
    resp = news_client.list_index_news(timeout=10)

    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200
