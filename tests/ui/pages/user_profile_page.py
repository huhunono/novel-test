"""Page Object for the user profile page (/user/userinfo.html).

Covers profile page navigation and user identity assertions.
This is a read-only page -- no state change risk.
"""
from playwright.sync_api import Page, expect


class UserProfilePage:

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        """Navigate to the user profile page."""
        self.page.goto(f"{self.base_url}/user/userinfo.html")

    def assert_profile_visible(self) -> None:
        """Verify the profile page has loaded (avatar and name area visible)."""
        expect(self.page.locator(".my_info")).to_be_visible()

    def assert_username_displayed(self, username: str) -> None:
        """Verify the displayed username matches the logged-in user."""
        expect(self.page.locator("#my_name")).to_have_text(username)
