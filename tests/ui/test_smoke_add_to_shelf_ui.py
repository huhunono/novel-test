"""UI smoke test for adding a book to the shelf.

This is a WRITE test -- it changes user data.
Idempotency strategy: remove the book from shelf first (if present),
then add it fresh. This ensures the test passes on every run.
"""
import pytest

from tests.data.users import VALID_USER
from tests.ui.flows.add_to_shelf_flow import AddToShelfFlow


@pytest.mark.ui
def test_smoke_add_to_shelf_ui(browser_page, base_url):
    """Search a book, add it to shelf, and verify it appears."""
    flow = AddToShelfFlow(browser_page, base_url)
    flow.login_search_and_add(VALID_USER["username"], VALID_USER["password"], "斗破苍穹")
