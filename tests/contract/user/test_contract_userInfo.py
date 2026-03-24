from jsonschema import validate
from schemas.endpoints.user.userInfo_response import USERINFO_RESPONSE
import pytest
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract


def test_contract_userinfo_response_schema(user_client):
    """
        Test Case: Verify User Information Retrieval Contract.

        Validation Logic:
        1. HTTP transport level (Status code 200 and JSON content-type).
        2. Global response format (ok=True, code=200).
        3. Full JSON Schema validation for user profile metadata (matches USERINFO_RESPONSE).
    """
    resp = user_client.user_info(allow_redirects=False, timeout=10)
    body = assert_json_response(resp)
    validate(instance=body, schema=USERINFO_RESPONSE)
    assert body["ok"] is True and body["code"] == 200


def test_contract_userinfo_unauthorized_returns_failure(base_url, plain_http):
    """
        Contract Test: Verify unauthenticated access to /user/userInfo is denied.

        Security boundary contract:
        - HTTP status must be 200, 401, or 403 (never 500)
        - If 200: ok=False, data=None (business-layer rejection)

        Moved from smoke/user — this is a behavioral contract check, not a
        liveness check. Smoke tests verify the service is up; contract tests
        verify the API enforces its authorization boundary.
    """
    resp = plain_http.get(base_url + "/user/userInfo", allow_redirects=False, timeout=10)
    assert resp.status_code in (200, 401, 403)
    if resp.status_code == 200:
        body = assert_json_response(resp)
        assert body.get("ok") is False
        assert body.get("data") is None


