import requests
from jsonschema import validate
from schemas.endpoints.book.list_rank_response import BOOK_RANK_ITEM_SCHEMA
import pytest

pytestmark = pytest.mark.contract

def test_contract_list_rank_schema(base_url):
    """
        Test Case: Verify Book Ranking List Contract.

        Validation Logic:
        1. HTTP transport level (Status code 200, JSON content-type, and explicitly no redirects).
        2. Global response format (ok=True, code=200).
        3. Book ranking list structure and item metadata consistency (matches BOOK_RANK_ITEM_SCHEMA).
    """
    param={"type":1}
    resp=requests.get(base_url+"/book/listRank",params=param,allow_redirects=False)
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")
    body = resp.json()
    validate(instance=body, schema=BOOK_RANK_ITEM_SCHEMA)
    assert body["ok"] is True and body["code"] == 200