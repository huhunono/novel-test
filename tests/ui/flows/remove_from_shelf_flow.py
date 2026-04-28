from playwright.sync_api import Page

from tests.ui.flows.add_to_shelf_flow import AddToShelfFlow
from tests.ui.pages.bookshelf_page import BookshelfPage


class RemoveFromShelfFlow:
    """Business flow for removing a book from the user's bookshelf.

    This is a WRITE operation that changes user data.
    To ensure the book exists before removal, it reuses AddToShelfFlow
    as a pre-condition setup step.
    """

    def __init__(self, page: Page, base_url: str):
        self.add_to_shelf_flow = AddToShelfFlow(page, base_url)
        self.shelf_page = BookshelfPage(page, base_url)

    def login_and_remove(self, username: str, password: str, keyword: str) -> None:
        """Ensure book is in shelf, then remove it and verify removal."""
        self.add_to_shelf_flow.login_search_and_add(username, password, keyword)
        self.shelf_page.open()
        self.shelf_page.remove_book_if_present(keyword)
        self.shelf_page.assert_book_not_in_shelf(keyword)