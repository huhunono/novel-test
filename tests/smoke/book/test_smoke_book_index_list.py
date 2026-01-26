import requests
import pytest
from tests.utils.assertions import assert_json_response
pytestmark = pytest.mark.smoke
def test_query_index_list(base_url,plain_http):
    """
        Smoke Test: Verify the Book Table of Contents (Index) API.

        Validates that the system can retrieve the chapter list for a specific book.
        This is a critical path for the reading experience; if this fails,
        users cannot access book content.
    """
    param={"bookId":2010824442059300864}
    resp = plain_http.get(base_url+"/book/queryIndexList", params=param,allow_redirects=False,timeout=10)
    body = assert_json_response(resp)
    assert body.get("ok") is True
    assert body.get("code") == 200

