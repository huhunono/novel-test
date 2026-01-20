import requests
from jsonschema import validate
from schemas.endpoints.book.query_index_response import QUERY_INDEX_LIST_RESPONSE_SCHEMA
import pytest

pytestmark = pytest.mark.contract

def test_contract_query_index_list_schema(base_url):
    """
        Test Case: Verify Book Chapter Index Pagination & Contract.

        Validation Logic:
        Ensures that for a given book, the system correctly returns a paginated list
        of chapters (TOC). This is critical for the reader's navigation flow.
    """
    param = {"bookId": 2010824442059300864}
    resp = requests.get(base_url + "/book/queryIndexList", params=param, allow_redirects=False)
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")
    body = resp.json()
    validate(instance=body, schema=QUERY_INDEX_LIST_RESPONSE_SCHEMA)
    assert body["ok"] is True and body["code"] == 200