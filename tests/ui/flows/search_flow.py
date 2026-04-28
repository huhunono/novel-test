from playwright.sync_api import Page

from tests.ui.pages.search_page import SearchPage


class SearchFlow:
    """Business flow for the search scenario.

    Verifies that searching a keyword returns visible results.
    Does not require login (search is a public feature).
    """

    def __init__(self, page: Page, base_url: str):
        self.search_page = SearchPage(page, base_url)

    def search_and_verify(self, keyword: str) -> None:
        """Open homepage, search a keyword, and assert results appear."""
        self.search_page.open()
        self.search_page.search(keyword)
        self.search_page.assert_search_success()