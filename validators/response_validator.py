"""
validators/response_validator.py

Composed response validation for API test assertions.

Responsibility:
- Validate HTTP status code and Content-Type (structural HTTP concerns).
- Optionally validate response body against a JSON Schema.
- Return the parsed body dict for further assertions by the caller.
- NOT responsible for business logic (ok=True, code=200, data fields).

Design note:
- Functions here are intentionally thin. They compose, not re-implement.
- assert_json_response is the single entry point for the vast majority of tests.
- assert_ok_true / assert_ok_false live here as canonical implementations;
  tests/utils/assertions.py re-exports them for backward compatibility.

Usage example:
    from validators.response_validator import assert_json_response, assert_ok_true

    body = assert_json_response(resp)
    assert_ok_true(body)
"""

from typing import Any, Dict, Optional

import requests

from validators.schema_validator import validate_schema


def assert_json_response(
    resp: requests.Response,
    expected_status: int = 200,
) -> Dict[str, Any]:
    """
    Assert the response is a valid HTTP 200 JSON response.

    Checks:
    1. HTTP status code equals *expected_status* (default 200).
    2. Content-Type header contains 'application/json'.
    3. Body is parseable as JSON.

    Args:
        resp:            The requests.Response object.
        expected_status: Expected HTTP status code (default 200).

    Returns:
        Parsed response body as dict.

    Raises:
        AssertionError on any check failure.
    """
    assert resp.status_code == expected_status, (
        f"Expected HTTP {expected_status}, got {resp.status_code}. "
        f"Body: {resp.text[:300]}"
    )

    ct = resp.headers.get("content-type", "")
    assert "application/json" in ct, (
        f"Expected application/json content-type, got: {ct!r}. "
        f"Body: {resp.text[:300]}"
    )

    return resp.json()


def assert_ok_true(body: Dict[str, Any]) -> None:
    """
    Assert the envelope field 'ok' is True.

    Args:
        body: Parsed JSON response body.

    Raises:
        AssertionError with full body on failure.
    """
    assert body.get("ok") is True, f"Expected ok=True, got: {body}"


def assert_ok_false(body: Dict[str, Any]) -> None:
    """
    Assert the envelope field 'ok' is False.

    Args:
        body: Parsed JSON response body.

    Raises:
        AssertionError with full body on failure.
    """
    assert body.get("ok") is False, f"Expected ok=False, got: {body}"


def assert_response_with_schema(
    resp: requests.Response,
    schema: Dict[str, Any],
    context: str = "",
    expected_status: int = 200,
) -> Dict[str, Any]:
    """
    Full contract validation: HTTP check + JSON Schema validation in one call.

    Intended for contract tests that want a single assertion call.

    Args:
        resp:            The requests.Response object.
        schema:          JSON Schema dict from schemas/endpoints/.
        context:         Optional label for error messages, e.g. "POST /user/login".
        expected_status: Expected HTTP status code (default 200).

    Returns:
        Parsed response body as dict.

    Raises:
        AssertionError on HTTP or schema failure.
    """
    body = assert_json_response(resp, expected_status=expected_status)
    validate_schema(body, schema, context=context)
    return body
