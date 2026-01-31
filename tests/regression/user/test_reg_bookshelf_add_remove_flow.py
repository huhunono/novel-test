import pytest
import requests
from tests.utils.assertions import assert_json_response,assert_ok_true

pytestmark = pytest.mark.regression

def is_truthy_shelf_flag(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v == 1
    if isinstance(v, str):
        return v.strip().lower() in ("1", "true")
    return None

def test_reg_bookshelf_add_remove_flow(base_url, auth_token):
    """
        Regression Test: End-to-End Bookshelf Lifecycle & Pagination Integrity.

        Logic Flow: Pre-clean -> Add -> State Verify -> Pagination Search -> Remove -> Post-verify.

        Checks:
        1) Idempotency & Setup: Ensures a clean starting state via proactive pre-deletion.
        2) State Flip: Validates 'queryIsInShelf' accurately reflects the book's presence.
        3) Pagination Discovery: Confirms that newly added books are correctly indexed in the
           paginated list API ('listBookShelfByPage').
        4) Environment Neutrality: Guarantees post-test cleanup via defensive try/finally.
        """

    # independent  session ensure that the state of this test does not contaminate others
    s=requests.Session()
    # update header with logged in token
    s.headers.update({"Authorization": auth_token})

    # assign existing book ID
    book_id = "2014580673134784512"

    # Pre-clean: ensure start state is "not in shelf"
    try:
        s.delete(f"{base_url}/user/removeFromBookShelf/{book_id}", allow_redirects=False, timeout=10)
    except Exception:
        pass

    # 1)  pre-check -> should be false (now controllable)
    resp_in=s.get(base_url + "/user/queryIsInShelf", params={"bookId": book_id}, allow_redirects=False)
    body_in=assert_json_response(resp_in)
    assert_ok_true(body_in)

    # update book state
    already_in = None
    data_in=body_in.get("data")

    #Defensive Logic:
    assert is_truthy_shelf_flag(body_in.get("data")) is False, body_in
    added= False
    # 2) main process ,try / finally ensure cleanup
    try:
        # 2.1 add to bookshelf , return response is not mandatory,make sure book in on the bookshelf
        resp_add= s.post(base_url + "/user/addToBookShelf", data={"bookId": book_id}, allow_redirects=False)
        body=assert_json_response(resp_add)
        assert_ok_true(body)
        assert body.get("code") == 200
        added=True

        # 2.2 queryIsInShelf, book must be existed in the bookshelf
        resp_in2= s.get(base_url + "/user/queryIsInShelf", params={"bookId": book_id}, allow_redirects=False)
        body_in2= assert_json_response(resp_in2)
        assert_ok_true(body_in2)
        assert is_truthy_shelf_flag(body_in2.get("data")) is True, body_in2

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
        resp_rm = s.delete(f"{base_url}/user/removeFromBookShelf/{book_id}", allow_redirects=False, timeout=10)
        body_rm = assert_json_response(resp_rm)
        assert_ok_true(body_rm)
        assert body_rm.get("code") == 200

        # 6) query -> false
        resp_in3 = s.get(base_url + "/user/queryIsInShelf", params={"bookId": book_id}, allow_redirects=False, timeout=10)
        body_in3 = assert_json_response(resp_in3)
        assert_ok_true(body_in3)
        assert is_truthy_shelf_flag(body_in3.get("data")) is False, body_in3
        added = False


    finally:
        # 3) Cleanup/Teardown: Restore the environment by removing the book
        if added:
            try:
                s.delete(f"{base_url}/user/removeFromBookShelf/{book_id}", allow_redirects=False, timeout=10)
            except Exception:
                pass







