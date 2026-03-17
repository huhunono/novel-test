import logging

import pytest

from clients.user_client import UserClient
from tests.utils.assertions import assert_json_response, assert_ok_true

pytestmark = pytest.mark.regression

logger = logging.getLogger(__name__)


@pytest.mark.xfail(
    reason="Known issue: non-existent bookId can be added; queryIsInShelf=true but listBookShelfByPage hides it (inconsistent contract)"
)
def test_reg_bookshelf_consistency_nonexistent_bookId_query_true_but_not_in_list(
    user_client: UserClient,
) -> None:
    """
        Regression Test: Verify Cross-API Data Consistency for Non-existent Book Resources.

        Logic Flow: addToBookShelf(nonexistent_id) → queryIsInShelf → listBookShelfByPage

        This test ensures that the bookshelf state is consistent across different query methods:
        1. Input Validation: Detects if the system erroneously allows non-existent book IDs to be added.
        2. State Synchronization: Verifies that if an API claims a book "is in shelf", it must actually appear in the shelf list.
        3. Contract Integrity: Identifies hidden inconsistencies where the write-path (add) and read-paths (query vs. list) disagree.
    """
    nonexistent_book_id: int = 999999999999
    target: str = str(nonexistent_book_id)

    try:
        # 1) add non-existent bookId (currently returns success)
        r1 = user_client.add_to_bookshelf(target, allow_redirects=False, timeout=10)
        b1 = assert_json_response(r1)
        assert_ok_true(b1)

        # 2) queryIsInShelf says true (current behavior)
        r2 = user_client.query_in_shelf(target, allow_redirects=False, timeout=10)
        b2 = assert_json_response(r2)
        assert_ok_true(b2)
        assert b2.get("data") is True

        # 3) listBookShelfByPage should be consistent with queryIsInShelf
        r3 = user_client.list_bookshelf_by_page(page_num=1, page_size=200, allow_redirects=False, timeout=10)
        b3 = assert_json_response(r3)
        assert_ok_true(b3)

        items = b3.get("data").get("list")
        in_list = any(str(x.get("bookId")) == target for x in items)
        assert in_list is True

    finally:
        # cleanup (even if asserts fail)
        try:
            user_client.remove_from_bookshelf(target, allow_redirects=False, timeout=10)
        except Exception:
            pass
