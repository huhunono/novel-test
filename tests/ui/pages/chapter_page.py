from playwright.sync_api import Page, expect


class ChapterPage:
    """Page Object for the chapter reading page.

    Verifies that chapter content has loaded and is not empty.
    """

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def assert_chapter_visible(self) -> None:
        """Verify the reading content area is visible and has content."""
        chapter = self.page.locator("#showReading")
        expect(chapter).to_be_visible()
        expect(chapter).not_to_be_empty()

