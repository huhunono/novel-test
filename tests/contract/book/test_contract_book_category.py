import requests
from jsonschema import validate
from schemas.endpoints.book.book_category_response import BOOK_CATEGORY_RESPONSE_SCHEMA
import pytest

pytestmark = pytest.mark.contract

def test_contract_book_category_schema(base_url):
    """
        Test Case: Verify Book Category List Contract.

        Validation Logic:
        1. HTTP transport level (Status code 200 and JSON content-type).
        2. Global response format (ok=True, code=200).
        3. Category tree or list structure consistency (matches BOOK_CATEGORY_RESPONSE_SCHEMA).
    """
    resp = requests.get(base_url + "/book/listBookCategory", allow_redirects=False)
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")
    body = resp.json()
    validate(instance=body,schema=BOOK_CATEGORY_RESPONSE_SCHEMA)
    assert body["ok"] is True and body["code"] == 200
