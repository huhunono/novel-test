"""UI smoke test for the book detail page.

Verifies that clicking a search result navigates to the book's
detail page with the title visible.
No login required (book detail is a public page).
"""
import pytest

from tests.ui.flows.book_detail_flow import BookDetailFlow


@pytest.mark.ui
def test_smoke_book_detail_ui(browser_page, base_url):
    """Search a book and verify its detail page loads correctly."""
    flow = BookDetailFlow(browser_page, base_url)
    flow.search_and_view_book_detail("斗破苍穹")
