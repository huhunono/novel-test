"""UI smoke test for bookshelf visibility after login.

Verifies that after a successful login, the 'My Bookshelf'
navigation link is visible on the page.
"""
import pytest

from tests.data.users import VALID_USER
from tests.ui.flows.bookshelf_flow import BookshelfFlow


@pytest.mark.ui
def test_smoke_bookshelf_ui(browser_page, base_url):
    """After login, the bookshelf navigation should be visible."""
    flow = BookshelfFlow(browser_page, base_url)
    flow.login_and_view_shelf(VALID_USER["username"], VALID_USER["password"])
