import requests
import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke
def test_query_book_detail(base_url,plain_http):
    """
        Smoke Test: Verify core availability of the Book Detail endpoint.

        This test ensures that a known valid book ID returns a successful
        response with the correct JSON structure. It serves as a health check
        for the primary business path.
    """

    book_id=2010824442059300864
    resp = plain_http.get(
        f"{base_url}/book/queryBookDetail/{book_id}", allow_redirects=False,timeout=10
    )
    body = assert_json_response(resp)


    # Assertion 3: Verify basic business success markers (Envelope Level)
    assert body.get("ok") is True
    assert body.get("code") == 200
    #data = body.get("data")
    #assert data is not None
    #id = data.get("id")
    #assert str(id) == str(book_id)




