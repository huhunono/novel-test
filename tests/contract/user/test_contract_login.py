import pytest
from jsonschema import validate

from schemas.endpoints.user.login_response import LOGIN_RESPONSE_DATA_SCHEMA
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract


def test_contract_login_response_schema(base_url, plain_http, test_user):
    """
        Test Case: Verify User Login Success Contract.

        Validation Logic:
        1. Global response format (ok=True, code=200).
        2. Authentication token presence and format in 'data' field.
        3. User profile metadata structure (matches LOGIN_RESPONSE_DATA_SCHEMA).
    """
    resp = plain_http.post(base_url + "/user/login", data=test_user, allow_redirects=False, timeout=10)
    body = assert_json_response(resp)
    validate(instance=body, schema=LOGIN_RESPONSE_DATA_SCHEMA)
    assert body["ok"] is True and body["code"] == 200


# NOTE: The negative login path (empty/wrong password → ok=False) is a
# business-behavior test, not a schema/contract test.
# It lives in: tests/regression/user/test_reg_login_invalid.py
# Contract tests only validate response schema structure.
