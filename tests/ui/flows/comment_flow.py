from playwright.sync_api import Page

from tests.ui.flows.auth_flow import AuthFlow
from tests.ui.pages.search_page import SearchPage
from tests.ui.pages.book_detail_page import BookDetailPage


class BookCommentFlow:
    """Business flow for verifying the comment form is usable.

    This flow intentionally does NOT submit the comment, because
    commenting is an irreversible state change (one comment per user
    per book, no delete button). Filling without submitting keeps
    this test safe for repeated CI runs.
    """

    def __init__(self, page: Page, base_url: str):
        self.auth = AuthFlow(page, base_url)
        self.search_page = SearchPage(page, base_url)
        self.detail_page = BookDetailPage(page, base_url)

    def login_search_and_fill_comment(
        self,
        username: str,
        password: str,
        keyword: str,
        content: str,
    ) -> None:
        """Log in, search a book, open detail, verify comment form, type draft."""
        self.auth.login_as(username, password)
        self.search_page.open()
        self.search_page.search(keyword)
        self.search_page.click_first_result()
        self.detail_page.assert_comment_form_ready()
        self.detail_page.fill_comment(content)