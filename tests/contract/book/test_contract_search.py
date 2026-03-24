from jsonschema import validate
from schemas.endpoints.book.search_response import SEARCH_BOOK_RESPONSE_SCHEMA
import pytest
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract

def test_contract_search_by_page_schema(book_client):
    """
        Test Case: Verify Book Search Pagination Contract.

        Validation Logic:
        1. Global response format (standard wrapper).
        2. Pagination metadata (pageNum, pageSize, total, etc.).
        3. Business entity data within the list (BOOK_ITEM_SCHEMA).
    """

    resp = book_client.search_by_page(
        page_num=1, page_size=20,
        extra_params={"keyword": "roman"},
        allow_redirects=False, timeout=10,
    )
    body = assert_json_response(resp)

    validate(instance=body,schema=SEARCH_BOOK_RESPONSE_SCHEMA)
    assert body["ok"] is True and body["code"] == 200



    '''
    assert isinstance(body, dict)
    assert body.get("ok") is True
    assert body.get("code") == 200

    data=body.get("data")
    assert data is not None
    assert isinstance(data, dict)

    for key in ["pageNum","pageSize","total","list","pages"]:
        assert key in data,f"missing key in data:{key}"

    assert isinstance(data["pageNum"],str)
    assert isinstance(data["pageSize"],str)
    assert isinstance(data["total"],str)
    assert isinstance(data["pages"],str)

    assert isinstance(data["list"],list)

    #if search result is found
    if data["list"]:
        first=data["list"][0]
        assert isinstance(first,dict)
        assert "id" in first
        assert "bookName" in first
        assert "authorName" in first
        
        '''
