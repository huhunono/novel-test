from typing import Dict

import pytest

from clients.base_client import BaseClient
from tests.utils.assertions import assert_json_response, assert_ok_true


@pytest.mark.reg_ci
def test_reg_ci_bookshelf_minimal_flow(base_url: str, test_user: Dict[str, str], plain_http: BaseClient) -> None:
    """
        CI Regression Test: Bookshelf lifecycle state machine.

        Logic Flow: Login -> Add -> Verify (True) -> Remove -> Verify (False)

        Checks:
        1) State Persistence: Verifies the backend correctly tracks book-to-user mapping.
        2) Boolean Consistency: Confirms 'isInShelf' flips precisely according to user actions.
        3) Resilient Cleanup: Uses nested try-finally to ensure environment neutrality
           post-execution, regardless of test outcome.

    """
    #1 login
    login_resp = plain_http.post(base_url + '/user/login', data=test_user, allow_redirects=False, timeout=20)
    login_body=assert_json_response(login_resp)
    assert_ok_true(login_body)
    assert login_body.get("code") == 200

    data=login_body.get("data")
    assert isinstance(data, dict)
    token=data.get("token")
    assert isinstance(token, str)
    assert token.strip()

    # update header
    plain_http.headers.update({"Authorization": token})
    book_id = 2010826914387599360

    try:
        # 2) add
        add_resp = plain_http.post(
            base_url + "/user/addToBookShelf",
            data={"bookId": book_id},
            allow_redirects=False,
            timeout=20,
        )
        add_body = assert_json_response(add_resp)
        assert_ok_true(add_body)
        assert add_body.get("code") == 200

        # 3) query -> true
        query_resp = plain_http.get(
            base_url + "/user/queryIsInShelf",
            params={"bookId": book_id},
            allow_redirects=False,
            timeout=20,
        )
        query_body = assert_json_response(query_resp)
        assert_ok_true(query_body)
        assert query_body.get("data") is True
        assert query_body.get("code") == 200

        # 4) remove
        remove_resp = plain_http.delete(
            f"{base_url}/user/removeFromBookShelf/{book_id}",
            allow_redirects=False,
            timeout=20,
        )
        remove_body = assert_json_response(remove_resp)
        assert_ok_true(remove_body)
        assert remove_body.get("code") == 200

        # 5) query -> false
        query_resp_2 = plain_http.get(
            base_url + "/user/queryIsInShelf",
            params={"bookId": book_id},
            allow_redirects=False,
            timeout=20,
        )
        query_body_2 = assert_json_response(query_resp_2)
        assert_ok_true(query_body_2)
        assert query_body_2.get("data") is False
        assert query_body_2.get("code") == 200

    finally:
        # cleanup best-effort only
        try:
            plain_http.delete(
                f"{base_url}/user/removeFromBookShelf/{book_id}",
                allow_redirects=False,
                timeout=10,
            )
        except Exception:
            pass







