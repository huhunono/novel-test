from playwright.sync_api import Page

from tests.ui.pages.book_detail_page import BookDetailPage
from tests.ui.pages.search_page import SearchPage


class BookDetailFlow:
    """Business flow for viewing a book's detail page.

    Searches for a book and navigates to its detail page.
    Spans two pages: SearchPage -> BookDetailPage.
    """

    def __init__(self, page: Page, base_url: str):
        self.detail_page = BookDetailPage(page, base_url)
        self.search_page = SearchPage(page, base_url)

    def search_and_view_book_detail(self, keyword: str) -> None:
        """Search a book, click the first result, verify detail page loads."""
        self.search_page.open()
        self.search_page.search(keyword)
        self.search_page.click_first_result()
        self.detail_page.assert_book_detail_visible()