import requests
from jsonschema import validate
from schemas.endpoints.book.book_detail_response import QUERY_BOOK_DETAIL_RESPONSE_SCHEMA
import pytest
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract


def test_contract_query_index_list_schema(base_url,plain_http):
    """
        Test Case: Verify Book Detail API Contract.

        Validation Logic:
        Check if the system returns correct metadata (author, category, description)
        for a specific book ID. This ensures the frontend info-page has all required data.
        """

    book_id = 2010824442059300864
    resp = plain_http.get(
        f"{base_url}/book/queryBookDetail/{book_id}", allow_redirects=False,timeout=10
    )
    body = assert_json_response(resp)
    validate(instance=body, schema=QUERY_BOOK_DETAIL_RESPONSE_SCHEMA)
    assert body["ok"]is True and body["code"]==200
