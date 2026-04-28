from playwright.sync_api import Page, expect


class SearchPage:
    """Page Object for the homepage search functionality.

    Handles keyword input, search submission, result clicking,
    and search result assertions.
    """

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        """Navigate to the homepage where the search bar lives."""
        self.page.goto(self.base_url)

    def search(self, keyword: str) -> None:
        """Type a keyword into the search box and submit."""
        self.page.get_by_placeholder("书名、作者、关键字").fill(keyword)
        self.page.locator("#btnSearch").click()

    def click_first_result(self) -> None:
        """Click the first book link in the search results table."""
        self.page.locator("#bookList tr .name a").first.click()

    def assert_search_success(self) -> None:
        """Verify at least one search result row is visible."""
        expect(self.page.locator("#bookList tr").first).to_be_visible()

