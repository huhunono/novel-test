import requests
from jsonschema import validate
from schemas.endpoints.user.userInfo_response import USERINFO_RESPONSE
import pytest

pytestmark = pytest.mark.contract

def test_contract_userinfo_response_schema(auth_http,base_url):
    """
        Test Case: Verify User Information Retrieval Contract.

        Validation Logic:
        1. HTTP transport level (Status code 200 and JSON content-type).
        2. Global response format (ok=True, code=200).
        3. Full JSON Schema validation for user profile metadata (matches USERINFO_RESPONSE).
    """
    resp=auth_http.get(base_url+"/user/userInfo")
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("content-type", "")
    body = resp.json()
    validate(instance=body,schema=USERINFO_RESPONSE)
    assert body["ok"] is True and body["code"] == 200


