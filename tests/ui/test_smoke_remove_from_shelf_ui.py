"""UI smoke test for removing a book from the shelf.

This is a WRITE test -- it changes user data.
Idempotency strategy: first ensure the book IS in the shelf
(by reusing AddToShelfFlow), then remove it and verify removal.
"""
import pytest

from tests.data.users import VALID_USER
from tests.ui.flows.remove_from_shelf_flow import RemoveFromShelfFlow


@pytest.mark.ui
def test_smoke_remove_from_shelf_ui(browser_page, base_url):
    """Ensure a book is in shelf, remove it, and verify it's gone."""
    flow = RemoveFromShelfFlow(browser_page, base_url)
    flow.login_and_remove(VALID_USER["username"], VALID_USER["password"], "斗破苍穹")
