import logging

import pytest

from clients.user_client import UserClient
from tests.data.books import BOOK_ID_IDEMPOTENT
from tests.utils.db_helpers import db_one
from tests.utils.assertions import assert_json_response, assert_ok_true

pytestmark = pytest.mark.regression

logger = logging.getLogger(__name__)


# ---------- Class B: Idempotency (State Control) ----------
def test_reg_addToBookShelf_idempotent_should_not_duplicate(
    user_client: UserClient,
    db_conn: object,
    test_user_id: int,
) -> None:
    """
        Regression Test: Verify API Idempotency for Add-to-Bookshelf Operations.

        Logic Flow: addToBookShelf (First Call) → addToBookShelf (Duplicate Call) → DB Verification

        This test ensures state consistency and prevents redundant data entry:
        1. Idempotency Validation: Ensures identical requests do not create duplicate records.
        2. Business Logic Integrity: Verifies the backend handles "already exists" scenario gracefully.
        3. Collection Accuracy: Confirms the book count in the shelf remains <= 1, preventing UI display bugs.
    """
    book_id: str = BOOK_ID_IDEMPOTENT

    try:
        # 1) same book added twice
        r1 = user_client.add_to_bookshelf(str(book_id), allow_redirects=False, timeout=10)
        b1 = assert_json_response(r1)
        assert_ok_true(b1)

        r2 = user_client.add_to_bookshelf(str(book_id), allow_redirects=False, timeout=10)
        b2 = assert_json_response(r2)
        assert_ok_true(b2)

        # 2) DB Validation: verify no duplicate records
        row = db_one(
            db_conn,
            "SELECT COUNT(*) AS c FROM user_bookshelf WHERE user_id=%s AND book_id=%s",
            (test_user_id, book_id),
        )
        assert row and "c" in row, "DB query failed: check user_bookshelf(user_id, book_id)"
        assert row["c"] <= 1

    finally:
        try:
            resp = user_client.remove_from_bookshelf(str(book_id), allow_redirects=False, timeout=10)
            if resp.status_code != 200:
                logger.warning("cleanup failed: status=%s body=%s", resp.status_code, resp.text[:200])
        except Exception as e:
            logger.warning("cleanup exception: %r", e)
