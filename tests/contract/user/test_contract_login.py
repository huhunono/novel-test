import pytest
import requests
from jsonschema import validate
from schemas.endpoints.user.login_response import LOGIN_RESPONSE_DATA_SCHEMA

pytestmark = pytest.mark.contract

def test_contract_login_response_schema(base_url):
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
    resp = requests.post(base_url +"/user/login", data=login_data, allow_redirects=False)
    assert resp.status_code == 200
    body = resp.json()

    validate(instance=body,schema=LOGIN_RESPONSE_DATA_SCHEMA)
    assert body["ok"] is True and body["code"] == 200

def test_contract_login_failure_schema(base_url):
    invalid_login_data={
        "username": "13560421999",
        "password": ""
    }
    resp = requests.post(base_url + "/user/login", data=invalid_login_data, allow_redirects=False)
    body = resp.json()
    assert body["ok"] is False
    assert body["data"] is None


