from typing import Dict

import pytest

from clients.user_client import UserClient
from tests.data.books import BOOK_ID_SHELF_CI
from tests.utils.assertions import assert_json_response, assert_ok_true


@pytest.mark.reg_ci
def test_reg_ci_bookshelf_minimal_flow(user_client: UserClient) -> None:
    """
        CI Regression Test: Bookshelf lifecycle state machine.

        Logic Flow: Add -> Verify (True) -> Remove -> Verify (False)

        Checks:
        1) State Persistence: Verifies the backend correctly tracks book-to-user mapping.
        2) Boolean Consistency: Confirms 'isInShelf' flips precisely according to user actions.
        3) Resilient Cleanup: Uses try-finally to ensure environment neutrality
           post-execution, regardless of test outcome.

        Note: Uses user_client fixture (auth already injected) instead of
        manually mutating plain_http headers, which would pollute fixture state.
    """
    book_id = BOOK_ID_SHELF_CI

    # Pre-clean: ensure deterministic start state
    try:
        user_client.remove_from_bookshelf(book_id, allow_redirects=False, timeout=10)
    except Exception:
        pass

    try:
        # 1) add
        add_resp = user_client.add_to_bookshelf(book_id, allow_redirects=False, timeout=20)
        add_body = assert_json_response(add_resp)
        assert_ok_true(add_body)
        assert add_body.get("code") == 200

        # 2) query -> true
        query_resp = user_client.query_in_shelf(book_id, allow_redirects=False, timeout=20)
        query_body = assert_json_response(query_resp)
        assert_ok_true(query_body)
        assert query_body.get("data") is True
        assert query_body.get("code") == 200

        # 3) remove
        remove_resp = user_client.remove_from_bookshelf(book_id, allow_redirects=False, timeout=20)
        remove_body = assert_json_response(remove_resp)
        assert_ok_true(remove_body)
        assert remove_body.get("code") == 200

        # 4) query -> false
        query_resp_2 = user_client.query_in_shelf(book_id, allow_redirects=False, timeout=20)
        query_body_2 = assert_json_response(query_resp_2)
        assert_ok_true(query_body_2)
        assert query_body_2.get("data") is False
        assert query_body_2.get("code") == 200

    finally:
        try:
            user_client.remove_from_bookshelf(book_id, allow_redirects=False, timeout=10)
        except Exception:
            pass







