import requests
from jsonschema import validate
from tests.schemas.common import BASE_RESPONSE_SCHEMA
from tests.schemas.pagination import pagination_schema
from tests.schemas.book import BOOK_DETAIL_SCHEMA
def test_query_index_list(base_url):
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
    #Structural Validation level 1
    validate(instance=body,schema=BASE_RESPONSE_SCHEMA)
    assert body["ok"]is True and body["code"]==200
    # Structural Validation level 2
    validate(instance=body["data"],schema=BOOK_DETAIL_SCHEMA)