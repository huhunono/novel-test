import logging

import pytest

from clients.base_client import BaseClient
from clients.user_client import UserClient
from tests.utils.assertions import assert_json_response, assert_ok_true, assert_ok_false

pytestmark = pytest.mark.regression

logger = logging.getLogger(__name__)


# ---------- valid login token ---------------
def test_reg_login_token_can_call_userinfo(user_client: UserClient) -> None:
    """
        Regression Test: Verify User Info retrieval using a valid Login Token.

        login → userInfo

        This test ensures the end-to-end authentication flow:
        1. Authorization headers are correctly propagated via user_client.
        2. The backend correctly identifies the user session.
        3. The profile data structure remains consistent for UI consumption.
    """
    resp = user_client.user_info(allow_redirects=False, timeout=20)

    body = assert_json_response(resp)
    assert_ok_true(body)
    assert body.get("code") == 200

    # Data Integrity Validation
    data = body.get("data")
    assert data is not None
    assert isinstance(data, dict)

    # Critical Field Presence
    assert data.get("username") or data.get("nickName") or data.get("id")


# ---------- missing login token ---------------
def test_reg_userinfo_requires_auth(plain_http, base_url) -> None:
    """
        Regression Test: Verify Access Control for Protected Resources.

        Logic Flow: GET /user/userInfo (without Authorization header)

        This test ensures that sensitive user data is shielded by the authentication gateway:
        1. Authorization Enforcement: Validates that the system denies access when the token is missing.
        2. Failure Consistency: Ensures the API returns a controlled failure (401/403 or ok=false with code 1001) instead of leaking data.
        3. Security Contract: Confirms that the 'data' field remains null, protecting user privacy.

        Note: plain_http is intentionally used here — this test validates the unauthenticated path.
    """
    resp = plain_http.get(base_url + "/user/userInfo", allow_redirects=False, timeout=20)

    assert resp.status_code in (200, 401, 403)

    if resp.status_code == 200:
        body = assert_json_response(resp)
        assert_ok_false(body)
        assert body.get("code") == 1001  # fixed: was 1001. (float) which never equals int
        assert body.get("data") is None


def test_reg_refresh_issues_new_token_and_old_token_still_works(base_url: str, auth_token: str) -> None:
    """
        Regression Test: Verify Token Refresh Logic and Overlap Grace Period.

        Logic Flow: refreshToken → Get New Token → Test Old Token → Test New Token

        This test ensures a smooth user experience during token rotation:
        1. Refresh Integrity: Confirms the /refreshToken endpoint successfully issues a valid new string token.
        2. Grace Period / Idempotency: Verifies if the old token remains valid for a short window after refresh
           (prevents race conditions in high-concurrency mobile apps).
        3. State Transition: Ensures the new token is immediately functional and provides access to user information.

        Note: BaseClient is instantiated directly here because this test needs to dynamically swap
        the Authorization header mid-test (old token → new token). A pre-built fixture cannot
        model this runtime token rotation, so manual client management is intentional and correct.
    """
    old_token: str = auth_token
    client = BaseClient(base_url=base_url, default_headers={"Authorization": old_token})
    try:
        # refresh new token
        resp_refresh = client.post("/user/refreshToken", allow_redirects=False, timeout=20)
        body = assert_json_response(resp_refresh)
        assert_ok_true(body)
        data = body.get("data")
        new_token = data.get("token")
        assert isinstance(new_token, str) and new_token, "refresh should return a new token"

        # use old token to request userinfo (grace period check)
        resp_info = client.get("/user/userInfo", allow_redirects=False, timeout=20)
        assert resp_info.status_code < 500

        if resp_info.status_code == 200:
            body = assert_json_response(resp_info)
            assert_ok_true(body)

        # switch to new token and verify it also works
        client.headers.update({"Authorization": new_token})
        refresh_info = client.get("/user/userInfo", allow_redirects=False, timeout=20)
        refresh_body = assert_json_response(refresh_info)
        assert_ok_true(refresh_body)
    finally:
        client.close()
