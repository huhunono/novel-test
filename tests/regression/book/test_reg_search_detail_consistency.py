import pytest

from tests.utils.assertions import assert_json_response,assert_ok_true

pytestmark = pytest.mark.regression

def _pick_first_book_from_search(body: dict) -> dict:
    data=body.get("data")
    assert isinstance(data,dict), data

    items=data.get("list")
    assert isinstance(items,list) and items, data

    # first book in the list
    book=items[0]
    assert isinstance(book, dict), book
    return book


def test_reg_search_to_detail_key_fields_consistent(auth_http, base_url):
    """
        Regression Test: Verify Data Consistency between Search Index and Book Details.

        Logic Flow: searchByPage → pick first book → queryBookDetail/{id}

        This test ensures synchronization between disparate data sources:
        1. Dynamic Discovery: Fetches real-time data from the search engine.
        2. Deep Link Validation: Verifies that the ID retrieved from search points to a valid detail page.
        3. Field Integrity: Ensures core metadata (Book Name, Author) matches exactly across different endpoints.
    """

    # 1) send searchByPage request
    params={"pageNum":1,"pageSize":10}
    resp_search=auth_http.get(base_url + "/book/searchByPage",params=params,allow_redirects=False)
    body_search=assert_json_response(resp_search)
    assert_ok_true(body_search)

    book=_pick_first_book_from_search(body_search)

    # get book id
    book_id=book.get("id")
    assert book_id is not None,book

    # Normalize IDs early
    book_id=str(book_id)

    search_book_name=book.get("bookName")
    search_author_name=book.get("authorName")

    # 2) queryBookDetail/{bookId}
    resp_detail = auth_http.get(base_url + f"/book/queryBookDetail/{book_id}", allow_redirects=False)
    body_detail = assert_json_response(resp_detail)
    assert_ok_true(body_detail)

    detail=body_detail.get("data")
    assert isinstance(detail,dict), detail

    detail_book_name=detail.get("bookName")
    detail_author_name=detail.get("authorName")

    if search_book_name is not None and detail_book_name is not None:
        assert str(search_book_name) == str(detail_book_name), (search_book_name, detail_book_name)

    if search_author_name is not None and detail_author_name is not None:
        assert str(detail_author_name) == str(search_author_name), (search_author_name, detail_author_name)




