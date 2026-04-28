from playwright.sync_api import Page

from tests.ui.pages.search_page import SearchPage
from tests.ui.pages.book_detail_page import BookDetailPage
from tests.ui.pages.chapter_page import ChapterPage


class ReadChapterFlow:
    """Business flow for reading the first chapter of a book.

    Searches for a book, opens its detail page, then navigates to
    chapter view. This is a read-only flow with no state change.
    Does not require login (chapters are publicly accessible).
    """

    def __init__(self, page: Page, base_url: str):
        self.detail_page = BookDetailPage(page, base_url)
        self.search_page = SearchPage(page, base_url)
        self.chapter_page = ChapterPage(page, base_url)

    def read_first_chapter(self, keyword: str) -> None:
        """Search a book, open detail, click first chapter, verify content."""
        self.search_page.open()
        self.search_page.search(keyword)
        self.search_page.click_first_result()
        self.detail_page.open_first_chapter()
        self.chapter_page.assert_chapter_visible()
