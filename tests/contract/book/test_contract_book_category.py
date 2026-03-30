import pytest

from schemas.endpoints.book.book_category_response import BOOK_CATEGORY_RESPONSE_SCHEMA
from tests.utils.assertions import assert_json_response
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.contract


def test_contract_book_category_schema(book_client):
    """
        Test Case: Verify Book Category List Contract.

        Validation Logic:
        1. HTTP transport level (Status code 200 and JSON content-type).
        2. Global response format (ok=True, code=200).
        3. Category tree or list structure consistency (matches BOOK_CATEGORY_RESPONSE_SCHEMA).
    """
    resp = book_client.list_categories(allow_redirects=False, timeout=10)
    body = assert_json_response(resp)
    validate_schema(body, BOOK_CATEGORY_RESPONSE_SCHEMA, context="GET /book/listBookCategory")
    assert body["ok"] is True and body["code"] == 200
