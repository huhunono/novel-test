import requests
from jsonschema import validate
from schemas.endpoints.book.book_detail_response import QUERY_BOOK_DETAIL_RESPONSE_SCHEMA
import pytest

pytestmark = pytest.mark.contract


def test_contract_query_index_list_schema(base_url):
    """
        Test Case: Verify Book Detail API Contract.

        Validation Logic:
        Check if the system returns correct metadata (author, category, description)
        for a specific book ID. This ensures the frontend info-page has all required data.
        """

    book_id = 2010824442059300864
    resp = requests.get(
        f"{base_url}/book/queryBookDetail/{book_id}", allow_redirects=False
    )
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")
    body = resp.json()
    validate(instance=body, schema=QUERY_BOOK_DETAIL_RESPONSE_SCHEMA)
    assert body["ok"]is True and body["code"]==200
