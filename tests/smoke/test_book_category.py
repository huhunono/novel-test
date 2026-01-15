import requests


def test_list_book_category_smoke(base_url):
    """
        Smoke Test: Verify the Book Category Lookup API.

        This interface provides the fundamental category list (e.g., Fantasy, Romance)
        used across the entire site. Failure here typically impacts navigation and search.
    """
    resp=requests.get(base_url+"/book/listBookCategory",allow_redirects=False)

    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")

    body = resp.json()
    assert body.get("ok") is True
    assert body.get("code") == 200
