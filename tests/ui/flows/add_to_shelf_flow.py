from playwright.sync_api import Page

from tests.ui.flows.auth_flow import AuthFlow
from tests.ui.pages.bookshelf_page import BookshelfPage
from tests.ui.pages.book_detail_page import BookDetailPage
from tests.ui.pages.search_page import SearchPage


class AddToShelfFlow:
    """Business flow for adding a book to the user's bookshelf.

    This is a WRITE operation that changes user data.
    To ensure idempotency (repeatable runs), it removes the book
    from the shelf first if already present, then adds it fresh.
    """

    def __init__(self, page: Page, base_url: str):
        self.auth = AuthFlow(page, base_url)
        self.shelf_page = BookshelfPage(page, base_url)
        self.search_page = SearchPage(page, base_url)
        self.detail_page = BookDetailPage(page, base_url)

    def login_search_and_add(self, username: str, password: str, keyword: str) -> None:
        """Log in, clean up shelf state, search the book, add it, then verify."""
        self.auth.login_as(username, password)

        # Pre-condition: remove the book if already in shelf to ensure a clean state
        self.shelf_page.open()
        self.shelf_page.remove_book_if_present(keyword)

        self.search_page.open()
        self.search_page.search(keyword)
        self.search_page.click_first_result()
        self.detail_page.add_to_bookshelf()

        self.shelf_page.open()
        self.shelf_page.assert_book_in_shelf(keyword)
