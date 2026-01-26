import pytest
import requests
from tests.utils.assertions import assert_json_response,assert_ok_true

pytestmark = pytest.mark.regression

def test_reg_bookshelf_add_remove_flow(base_url, auth_token):
    """
        Regression Test: Complete Bookshelf Lifecycle (Add -> List -> Remove).

        Logic Flow: queryIsInShelf -> addToBookShelf -> listBookShelfByPage -> removeFromBookShelf

        This test ensures business consistency for the bookshelf module:
        1. Pre-check: Determine initial state to prevent environmental contamination.
        2. Atomic Operation: Adding a book must reflect immediately in status queries.
        3. Data Consistency: The added book must appear in the paginated bookshelf list.
        4. Teardown/Cleanup: Removing the book must return the state to False/0.
    """

    # independent  session ensure that the state of this test does not contaminate others
    s=requests.Session()
    # update header with logged in token
    s.headers.update({"Authorization": auth_token})

    # assign existing book ID
    book_id = "2014580673134784512"

    # 1) Is the book on the bookshelf?
    resp_in=s.get(base_url + "/user/queryIsInShelf", params={"bookId": book_id}, allow_redirects=False)
    body_in=assert_json_response(resp_in)
    assert_ok_true(body_in)

    # update book state
    already_in = None
    data_in=body_in.get("data")

    #Defensive Logic:
    if isinstance(data_in,bool):
        already_in = data_in
    elif isinstance(data_in,(int,str)):
        already_in = str(data_in) in ("1","true","True","TRUE")
    else:
        already_in = None

    # 2) main process ,try / finally ensure cleanup
    try:
        # 2.1 add to bookshelf , return response is not mandatory,make sure book in on the bookshelf
        resp_add= s.post(base_url + "/user/addToBookShelf", data={"bookId": book_id}, allow_redirects=False)
        body=assert_json_response(resp_add)

        # 2.2 queryIsInShelf, book must be existed in the bookshelf
        resp_in2= s.get(base_url + "/user/queryIsInShelf", params={"bookId": book_id}, allow_redirects=False)
        body_in2= assert_json_response(resp_in2)
        assert_ok_true(body_in2)
        assert str(body_in2.get("data")).lower() in ("true","1"),body_in2

        # 2.3 listBookShelfByPage must include the bookId
        found = False
        # look for first 5 pages
        for page in range(1,6):
            resp_list=s.get(base_url + "/user/listBookShelfByPage",params={"pageNum": page, "pageSize": 20})
            body_list=assert_json_response(resp_list)
            assert_ok_true(body_list)
            data_list = body_list.get("data")
            assert isinstance(data_list, dict), f"data is not dict: {data_list}"
            items = data_list.get("list")
            assert isinstance(items, list), f"list is not list: {items}"
            for x in items:
                if str(x["bookId"]) == str(book_id):
                    found = True
                    break
        assert found, f"bookId {book_id} not found in first 5 pages"

    finally:
        # 3) Cleanup/Teardown: Restore the environment by removing the book
        # This block runs even if the assertions above fail
        resp_rm=s.delete(f"{base_url}/user/removeFromBookShelf/{book_id}",allow_redirects=False)
        body_rm=assert_json_response(resp_rm)
        assert_ok_true(body_rm)

        # 4) Final Verification: Ensure the book is successfully removed
        resp_in3 = s.get(base_url + "/user/queryIsInShelf", params={"bookId": book_id}, allow_redirects=False)
        body_in3 = assert_json_response(resp_in3)
        assert_ok_true(body_in3)
        assert str(body_in3.get("data")).lower() in ("false", "0", "none", "null"), body_in3







