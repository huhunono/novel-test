import pytest

from tests.data.users import TEST_USERNAME
from tests.utils.db_helpers import db_one

pytestmark = pytest.mark.regression


def test_reg_login_user_exists_in_db(db_conn, test_user_id: int) -> None:
    """
    Regression Test: Verify test user identity at the DB layer.

    Confirms the authenticated test user has a correct record in the user
    table. Guards against environment misconfiguration where the credential
    works at the API level but the DB record is missing or corrupted.
    """
    row = db_one(
        db_conn,
        "SELECT id, username FROM user WHERE id = %s",
        (test_user_id,),
    )
    assert row is not None, f"No user row found in DB for id={test_user_id}"
    assert row["username"] == TEST_USERNAME, (
        f"DB username mismatch: expected={TEST_USERNAME!r}, got={row['username']!r}"
    )
