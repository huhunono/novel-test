"""UI smoke tests for the login page.

Covers two scenarios:
- Happy path: valid credentials -> redirect to homepage
- Error path: wrong password -> stay on login page with error message
"""
import pytest

from tests.data.users import VALID_USER
from tests.ui.flows.auth_flow import AuthFlow


@pytest.mark.ui
def test_smoke_login_ui(browser_page, base_url):
    """Valid credentials should log the user in successfully."""
    auth_flow = AuthFlow(browser_page, base_url)
    auth_flow.login_as(VALID_USER["username"], VALID_USER["password"])


@pytest.mark.ui
def test_smoke_login_invalid_ui(browser_page, base_url):
    """Wrong password should show an error and stay on the login page."""
    auth_flow = AuthFlow(browser_page, base_url)
    auth_flow.login_failed(VALID_USER["username"], "wrong_password")
