import requests
import pytest

pytestmark = pytest.mark.smoke
def test_list_rank(base_url):
    """
        Smoke Test: Verify the Book Ranking List API.

        This test checks the system's ability to retrieve ranking data
        (e.g., 1 for Top Clicked, 2 forTop New Books) which is essential for the homepage.

    """
    param={"type":1}
    resp=requests.get(base_url+"/book/listRank",params=param,allow_redirects=False)
    assert resp.status_code == 200
    ct = resp.headers.get("content-type", "")
    if "application/json" not in ct:
        raise AssertionError(
            "Content type is not application/json.\n"f"url:{resp.request.url}\n"f"status:{resp.status_code}\n"
            f"ct:{ct}\n"
            f"text:{resp.text[:300]}\n")
    body = resp.json()
    assert body.get("ok") is True
    assert body.get("code") == 200
    #data = body.get("data")
    #assert data is not None
    #assert isinstance(data, list)
    #assert len(data) >= 1
    #first = data[0]
    #assert "id" in first
    #assert "bookName" in first or "book_name" in first