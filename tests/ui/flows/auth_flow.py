from playwright.sync_api import Page

from tests.ui.pages.login_page import LoginPage


class AuthFlow:
    """Business flow for authentication scenarios.

    Orchestrates LoginPage to perform complete login workflows.
    Used by other flows that require a logged-in user as pre-condition.
    """

    def __init__(self, page: Page, base_url: str):
        self.login_page = LoginPage(page, base_url)

    def login_as(self, username: str, password: str) -> None:
        """Log in with valid credentials and verify success."""
        self.login_page.open()
        self.login_page.login(username, password)
        self.login_page.assert_login_success()

    def login_failed(self, username: str, password: str) -> None:
        """Attempt login with invalid credentials and verify failure."""
        self.login_page.open()
        self.login_page.login(username, password)
        self.login_page.assert_login_failed()
