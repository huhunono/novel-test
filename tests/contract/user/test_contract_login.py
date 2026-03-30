import pytest

from schemas.endpoints.user.login_response import LOGIN_RESPONSE_DATA_SCHEMA
from tests.utils.assertions import assert_json_response
from validators.schema_validator import validate_schema

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
    validate_schema(body, LOGIN_RESPONSE_DATA_SCHEMA, context="POST /user/login")
    assert body["ok"] is True and body["code"] == 200
