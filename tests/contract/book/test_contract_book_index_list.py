import requests
from jsonschema import validate
from schemas.endpoints.book.query_index_response import QUERY_INDEX_LIST_RESPONSE_SCHEMA
import pytest
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract

def test_contract_query_index_list_schema(base_url,plain_http):
    """
        Test Case: Verify Book Chapter Index Pagination & Contract.

        Validation Logic:
        Ensures that for a given book, the system correctly returns a paginated list
        of chapters (TOC). This is critical for the reader's navigation flow.
    """
    param = {"bookId": 2010824442059300864}
    resp = plain_http.get(base_url + "/book/queryIndexList", params=param, allow_redirects=False,timeout=10)
    body = assert_json_response(resp)
    validate(instance=body, schema=QUERY_INDEX_LIST_RESPONSE_SCHEMA)
    assert body["ok"] is True and body["code"] == 200