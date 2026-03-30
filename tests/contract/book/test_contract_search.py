import pytest

from schemas.endpoints.book.search_response import SEARCH_BOOK_RESPONSE_SCHEMA
from tests.utils.assertions import assert_json_response
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.contract


def test_contract_search_by_page_schema(book_client):
    """
        Test Case: Verify Book Search Pagination Contract.

        Validation Logic:
        1. Global response format (standard wrapper).
        2. Pagination metadata (pageNum, pageSize, total, etc.).
        3. Business entity data within the list (BOOK_ITEM_SCHEMA).
    """
    resp = book_client.search_by_page(
        page_num=1, page_size=20,
        extra_params={"keyword": "roman"},
        allow_redirects=False, timeout=10,
    )
    body = assert_json_response(resp)
    validate_schema(body, SEARCH_BOOK_RESPONSE_SCHEMA, context="GET /book/searchByPage")
    assert body["ok"] is True and body["code"] == 200
