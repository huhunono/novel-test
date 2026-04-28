from playwright.sync_api import Page

from tests.ui.flows.auth_flow import AuthFlow
from tests.ui.pages.bookshelf_page import BookshelfPage


class BookshelfFlow:
    """Business flow for viewing the bookshelf after login.

    Reuses AuthFlow to log in, then checks that the shelf is accessible.
    This is a read-only flow with no state change.
    """

    def __init__(self, page: Page, base_url: str):
        self.auth = AuthFlow(page, base_url)
        self.shelf_page = BookshelfPage(page, base_url)

    def login_and_view_shelf(self, username: str, password: str) -> None:
        """Log in and verify the bookshelf navigation is visible."""
        self.auth.login_as(username, password)
        self.shelf_page.assert_shelf_visible()