import requests
from jsonschema import validate
from tests.schemas.common import BASE_RESPONSE_SCHEMA
from tests.schemas.pagination import pagination_schema
from tests.schemas.index import BOOK_INDEX_SCHEMA
def test_query_index_list(base_url):
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
    validate(instance=body,schema=BASE_RESPONSE_SCHEMA)
    assert body["ok"] is True and body["code"] == 200
    validate(instance=body["data"],schema=pagination_schema(BOOK_INDEX_SCHEMA))