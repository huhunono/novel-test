from jsonschema import validate
from schemas.endpoints.book.list_rank_response import BOOK_RANK_ITEM_SCHEMA
import pytest
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract

def test_contract_list_rank_schema(book_client):
    """
        Test Case: Verify Book Ranking List Contract.

        Validation Logic:
        1. HTTP transport level (Status code 200, JSON content-type, and explicitly no redirects).
        2. Global response format (ok=True, code=200).
        3. Book ranking list structure and item metadata consistency (matches BOOK_RANK_ITEM_SCHEMA).
    """
    resp = book_client.list_rank(type_=1, allow_redirects=False, timeout=10)
    body = assert_json_response(resp)
    validate(instance=body, schema=BOOK_RANK_ITEM_SCHEMA)
    assert body["ok"] is True and body["code"] == 200