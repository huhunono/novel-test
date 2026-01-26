import pytest
import requests
from jsonschema import validate
from schemas.endpoints.user.login_response import LOGIN_RESPONSE_DATA_SCHEMA
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract

def test_contract_login_response_schema(base_url,plain_http):
    """
        Test Case: Verify User Login Success Contract.

        Validation Logic:
        1. Global response format (ok=True, code=200).
        2. Authentication token presence and format in 'data' field.
        3. User profile metadata structure (matches LOGIN_RESPONSE_DATA_SCHEMA).
    """

    login_data={
        "username": "13560421999",
        "password": "123456"
    }
    resp = plain_http.post(base_url +"/user/login", data=login_data, allow_redirects=False,timeout=10)
    body = assert_json_response(resp)

    validate(instance=body,schema=LOGIN_RESPONSE_DATA_SCHEMA)
    assert body["ok"] is True and body["code"] == 200

def test_contract_login_failure_schema(base_url,plain_http):
    invalid_login_data={
        "username": "13560421999",
        "password": ""
    }
    resp = plain_http.post(base_url + "/user/login", data=invalid_login_data, allow_redirects=False,timeout=10)
    assert resp.status_code in (200, 400, 401, 422)

    body = resp.json()
    assert body["ok"] is False
    assert body["data"] is None


