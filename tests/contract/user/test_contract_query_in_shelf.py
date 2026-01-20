from jsonschema import validate
import pytest
from schemas.base.response import BASE_RESPONSE_SCHEMA

pytestmark = pytest.mark.contract

def test_contract_query_in_shelf_response_schema(auth_http,base_url):
    """
        Test Case: Verify Book In-Shelf Status Contract.

        Validation Logic:
        1. HTTP transport level (Status code 200 and JSON content-type).
        2. Global response format (matches BASE_RESPONSE_SCHEMA).
        3. Presence of 'data' field and confirmation of Boolean status (True).
    """
    book_id = {"bookId": 2010824442059300864}
    resp=auth_http.get(base_url+"/user/queryIsInShelf",params=book_id,allow_redirects=False)
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("content-type", "")
    body = resp.json()
    validate(instance=body,schema=BASE_RESPONSE_SCHEMA)
    assert "data" in body
    assert body["data"] is True
