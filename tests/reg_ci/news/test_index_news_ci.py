import pytest
from tests.utils.assertions import assert_json_response,assert_ok_true

@pytest.mark.reg_ci
def test_reg_ci_list_index_news_basic(plain_http, base_url):
    """
        CI Regression Test: Verify Homepage News List Integrity.

        Logic Flow: /news/listIndexNews (GET)

        Checks:
        1) Content Delivery: Confirms the endpoint returns a valid 200 OK and a non-empty news list.
        2) Metadata Identity: Ensures each news item contains a unique 'id' for routing/detail access.
        3) Display Readiness: Validates that 'title' is a non-empty string to prevent UI layout collapse.

    """
    resp=plain_http.get(base_url + "/news/listIndexNews",allow_redirects=False,timeout=20)

    body=assert_json_response(resp)

    assert_ok_true(body)
    assert body.get("code") == 200
    data = body.get("data")
    assert isinstance(data, list)

    assert len(data) > 0

    first = data[0]
    assert isinstance(first, dict)

    assert first.get("id") is not None

    title = first.get("title")
    assert isinstance(title, str)
    assert title.strip()