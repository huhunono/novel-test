import pytest
from jsonschema import validate

from schemas.endpoints.book.query_index_response import QUERY_INDEX_LIST_RESPONSE_SCHEMA
from tests.data.books import BOOK_ID_DETAIL
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract


def test_contract_query_index_list_schema(book_client):
    """
        Test Case: Verify Book Chapter Index Pagination & Contract.

        Validation Logic:
        Ensures that for a given book, the system correctly returns a paginated list
        of chapters (TOC). This is critical for the reader's navigation flow.
    """
    resp = book_client.query_index_list(
        str(BOOK_ID_DETAIL), allow_redirects=False, timeout=10
    )
    body = assert_json_response(resp)
    validate(instance=body, schema=QUERY_INDEX_LIST_RESPONSE_SCHEMA)
    assert body["ok"] is True and body["code"] == 200
