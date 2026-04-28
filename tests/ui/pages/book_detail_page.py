from playwright.sync_api import Page, expect


class BookDetailPage:
    """Page Object for the book detail page (/book/{id}.html).

    Covers book info assertions, bookshelf actions, chapter navigation,
    and comment form interactions.
    Note: fill_comment() intentionally does NOT submit to avoid
    irreversible state changes (one comment per user per book).
    """

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def assert_book_detail_visible(self) -> None:
        """Verify the book title heading is displayed."""
        expect(self.page.locator(".book_info .tit h1")).to_be_visible()

    def add_to_bookshelf(self) -> None:
        """Click 'Add to Shelf' and wait for the backend to persist."""
        self.page.get_by_role("link", name="加入书架").click()
        self.page.wait_for_timeout(1500)

    def open_first_chapter(self) -> None:
        """Click the 'Start Reading' link to enter chapter view."""
        self.page.get_by_role("link", name="点击阅读").click()

    def assert_comment_form_ready(self) -> None:
        """Verify the comment textarea and submit button are visible."""
        expect(self.page.locator("#txtComment")).to_be_visible()
        expect(self.page.locator("a.btn_ora", has_text="发表")).to_be_visible()

    def fill_comment(self, content: str) -> None:
        """Type content into the comment box WITHOUT submitting."""
        self.page.locator("#txtComment").fill(content)
        expect(self.page.locator("#txtComment")).to_have_value(content)