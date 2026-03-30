import pytest

from schemas.endpoints.book.list_rank_response import BOOK_RANK_ITEM_SCHEMA
from tests.utils.assertions import assert_json_response
from validators.schema_validator import validate_schema

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
    validate_schema(body, BOOK_RANK_ITEM_SCHEMA, context="GET /book/listRank")
    assert body["ok"] is True and body["code"] == 200
