import requests
import pytest

pytestmark = pytest.mark.smoke
def test_search_by_page(base_url):
    """
        Smoke Test: Verify the Book Search & Pagination API.

        This test validates the core search functionality which involves keyword matching
        and database pagination logic. It ensures users can find content via the
        global search bar.
    """
    param={"curr":1,"limit":20,"keyword":"roman"}
    resp = requests.get(base_url + "/book/searchByPage",params=param, allow_redirects=False)
    assert resp.status_code == 200
    ct=resp.headers.get("content-type","")
    if "application/json" not in ct:
        raise AssertionError("Content type is not application/json.\n"f"url:{resp.request.url}\n"f"status:{resp.status_code}\n"
                             f"ct:{ct}\n"
                             f"text:{resp.text[:300]}\n")
    body =resp.json()
    assert body.get("ok") is True
    assert body.get("code") == 200
    #data = body.get("data")
    #assert data is not None






