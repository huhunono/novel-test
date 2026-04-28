from playwright.sync_api import Page, expect


class BookshelfPage:
    """Page Object for the bookshelf page (/user/favorites.html).

    Handles shelf visibility, book presence checks, and add/remove
    operations. Supports idempotent test patterns via
    remove_book_if_present() for pre-condition cleanup.
    """

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        """Navigate to the user's bookshelf page."""
        self.page.goto(f"{self.base_url}/user/favorites.html")

    def assert_shelf_visible(self) -> None:
        """Verify the 'My Bookshelf' navigation link is visible."""
        expect(self.page.get_by_role("link", name="我的书架")).to_be_visible()

    def is_book_in_shelf(self, book_name: str) -> bool:
        """Return True if the book appears in the shelf list (no assertion)."""
        return self.page.locator("#bookShelfList td.name a").filter(has_text=book_name).count() > 0

    def remove_book_if_present(self, book_name: str) -> None:
        """Remove a book from shelf only if it exists. Safe to call anytime."""
        row = self.page.locator("#bookShelfList tr").filter(has_text=book_name)
        if row.count() > 0:
            row.get_by_role("link", name="移出书架").click()
            self.page.wait_for_timeout(1000)

    def assert_book_in_shelf(self, book_name: str) -> None:
        """Assert the book IS present in the shelf list."""
        expect(self.page.locator(f"#bookShelfList td.name a:has-text('{book_name}')")).to_be_visible()

    def assert_book_not_in_shelf(self, book_name: str) -> None:
        """Assert the book is NOT present in the shelf list."""
        expect(self.page.locator(f"#bookShelfList td.name a:has-text('{book_name}')")).not_to_be_visible()