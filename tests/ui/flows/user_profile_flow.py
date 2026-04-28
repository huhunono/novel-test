"""Business flow for viewing the user profile after login.

Reuses AuthFlow to log in, then navigates to the profile page
and verifies the correct username is displayed.
This is a read-only flow with no state change.
"""
from playwright.sync_api import Page

from tests.ui.flows.auth_flow import AuthFlow
from tests.ui.pages.user_profile_page import UserProfilePage


class UserProfileFlow:

    def __init__(self, page: Page, base_url: str):
        self.auth = AuthFlow(page, base_url)
        self.profile_page = UserProfilePage(page, base_url)

    def login_and_view_profile(self, username: str, password: str) -> None:
        """Log in, open the profile page, and verify the username matches."""
        self.auth.login_as(username, password)
        self.profile_page.open()
        self.profile_page.assert_profile_visible()
        self.profile_page.assert_username_displayed(username)
