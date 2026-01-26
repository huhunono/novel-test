import pytest
from tests.utils.assertions import assert_json_response,assert_ok_true
from tests.regression.book.test_reg_search_detail_consistency import _pick_first_book_from_search

pytestmark = pytest.mark.regression

def test_reg_detail_to_indexlist_bookid_consistent(auth_http, base_url):
    """
        Regression Test: Verify Foreign Key Integrity between Book Details and Chapter Index.

        Logic Flow: searchByPage → queryBookDetail → queryIndexList

        This test ensures the hierarchical data integrity:
        1. Dynamic Linking: Confirms that a valid book discovered via search has a retrievable detail page.
        2. Relational Consistency: Validates that every chapter/index entry returned by 'queryIndexList'
           belongs strictly to the requested 'bookId'.
        3. Child-Parent Mapping: Guarantees that the backend correctly filters content based on the parent ID.

    """
    # 1) searchByPage
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


    # 2) queryBookDetail/{bookId}
    resp_detail = auth_http.get(base_url + f"/book/queryBookDetail/{book_id}", allow_redirects=False)
    body_detail = assert_json_response(resp_detail)
    assert_ok_true(body_detail)

    detail=body_detail.get("data")
    assert isinstance(detail,dict), detail

    # 3) indexList
    resp_index = auth_http.get(base_url + "/book/queryIndexList",params={"bookId": book_id},allow_redirects=False)
    body_index = assert_json_response(resp_index)
    assert_ok_true(body_index)

    data_index=body_index.get("data")
    assert data_index is not None,data_index
    assert isinstance(data_index,dict), data_index

    item_index=data_index.get("list")
    assert isinstance(item_index, list), item_index

    checked = 0
    for it in item_index:
        if not isinstance(it, dict):
            continue
        if "bookId" not in it:
            continue
        checked += 1
        assert str(it["bookId"]) == book_id, {"expected": book_id, "got": it.get("bookId"), "item": it}

    assert checked > 0, {"bookId": book_id, "items_preview": item_index[:2]}