import pytest
from jsonschema import validate

from schemas.endpoints.book.book_detail_response import QUERY_BOOK_DETAIL_RESPONSE_SCHEMA
from tests.data.books import BOOK_ID_DETAIL
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract


def test_contract_query_index_list_schema(book_client):
    """
        Test Case: Verify Book Detail API Contract.

        Validation Logic:
        Check if the system returns correct metadata (author, category, description)
        for a specific book ID. This ensures the frontend info-page has all required data.
        """
    resp = book_client.query_detail(str(BOOK_ID_DETAIL), allow_redirects=False, timeout=10)
    body = assert_json_response(resp)
    validate(instance=body, schema=QUERY_BOOK_DETAIL_RESPONSE_SCHEMA)
    assert body["ok"] is True and body["code"] == 200
