import requests
from jsonschema import validate
from schemas.endpoints.book.book_category_response import BOOK_CATEGORY_RESPONSE_SCHEMA
import pytest
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract

def test_contract_book_category_schema(base_url,plain_http):
    """
        Test Case: Verify Book Category List Contract.

        Validation Logic:
        1. HTTP transport level (Status code 200 and JSON content-type).
        2. Global response format (ok=True, code=200).
        3. Category tree or list structure consistency (matches BOOK_CATEGORY_RESPONSE_SCHEMA).
    """
    resp = plain_http.get(base_url + "/book/listBookCategory", allow_redirects=False,timeout=10)
    body = assert_json_response(resp)
    validate(instance=body,schema=BOOK_CATEGORY_RESPONSE_SCHEMA)
    assert body["ok"] is True and body["code"] == 200
