import pytest
from schemas.endpoints.user.list_book_shelf_response import BOOK_SHELF_RESPONSE_SCHEMA
from jsonschema import validate
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract

def test_contract_book_shelf_response_schema(user_client):
    """
        Test Case: Verify User Bookshelf Paginated List Contract.

        Validation Logic:
        1. HTTP transport level (Status code 200 and JSON content-type).
        2. Global response format (ok=True, code=200).
        3. Paginated data structure and book item metadata (matches BOOK_SHELF_RESPONSE_SCHEMA).
    """
    resp = user_client.list_bookshelf_by_page(allow_redirects=False, timeout=10)
    body = assert_json_response(resp)
    validate(instance=body,schema=BOOK_SHELF_RESPONSE_SCHEMA)
    assert body["ok"] is True and body["code"] == 200