import requests
import pytest

pytestmark = pytest.mark.smoke

def test_index_news(base_url):
    """
        Smoke Test: Verify the Index News API is reachable and returns a valid response.

        This test ensures that the core news service is functional without performing
        deep data validation.
    """
    resp=requests.get(base_url+"/news/listIndexNews")
    assert resp.status_code == 200
    ct=resp.headers.get("content-type","")
    if "application/json" not in ct:
        raise AssertionError("Content type is not application/json.\n"f"url:{resp.request.url}\n"f"status:{resp.status_code}\n"
                             f"ct:{ct}\n"
                             f"text:{resp.text[:300]}\n")
    body =resp.json()
    assert body.get("ok") is True
    assert body.get("code") == 200
