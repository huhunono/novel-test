"""UI smoke test for the user profile page.

Verifies that after login, the profile page displays the correct
username (phone number). This is a read-only test with no state change.
"""
import pytest

from tests.data.users import VALID_USER
from tests.ui.flows.user_profile_flow import UserProfileFlow


@pytest.mark.ui
def test_smoke_user_profile_ui(browser_page, base_url):
    """After login, the profile page should show the user's phone number."""
    flow = UserProfileFlow(browser_page, base_url)
    flow.login_and_view_profile(VALID_USER["username"], VALID_USER["password"])
