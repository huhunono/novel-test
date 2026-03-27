from typing import Dict

import pytest

from clients.user_client import UserClient
from tests.utils.assertions import assert_json_response, assert_ok_true


@pytest.mark.reg_ci
def test_reg_ci_login_and_token_usable(user_client: UserClient, test_user: Dict[str, str]) -> None:
    """
        CI Regression Test: Authentication Flow and Token Usability.

        Logic Flow: login (via session fixture) -> /user/userInfo (GET)

        Checks:
        1) Authentication: Verifies that valid credentials yield a usable token (handled by auth_token fixture).
        2) Identity Persistence: Validates that the 'userInfo' retrieved via the token
           correctly matches the logged-in user.

        Note: This test uses user_client fixture (auth already injected) instead of
        manually mutating plain_http headers, which would pollute fixture state
        for other tests in the same session.
    """
    resp = user_client.user_info(allow_redirects=False, timeout=20)
    body = assert_json_response(resp)
    assert_ok_true(body)
    assert body.get("code") == 200

    user_data = body.get("data")
    assert isinstance(user_data, dict)
    assert user_data.get("username") == test_user.get("username")
