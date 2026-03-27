import pytest

from tests.data.books import BOOK_ID_DETAIL
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.smoke


def test_query_book_detail(book_client):
    """
        Smoke Test: Verify core availability of the Book Detail endpoint.

        This test ensures that a known valid book ID returns a successful
        response with the correct JSON structure. It serves as a health check
        for the primary business path.
    """
    resp = book_client.query_detail(str(BOOK_ID_DETAIL), allow_redirects=False, timeout=10)
    body = assert_json_response(resp)

    # Assertion 3: Verify basic business success markers (Envelope Level)
    assert body.get("ok") is True
    assert body.get("code") == 200
    #data = body.get("data")
    #assert data is 