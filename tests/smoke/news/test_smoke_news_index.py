import os

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

    print("NEWS_DEBUG BASE_URL=", os.getenv("BASE_URL"))
    print("NEWS_DEBUG resp.url=", resp.url)
    print("NEWS_DEBUG status_code=", resp.status_code)
    print("NEWS_DEBUG content-type=", resp.headers.get("content-type"))
    print("NEWS_DEBUG body[:300]=", resp.text[:300])

    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200
    assert body.get("data") is not None, f"data is null: {body}"
