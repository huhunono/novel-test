"""
validators/schema_validator.py

Thin wrapper around jsonschema.validate() for use in contract tests.

Responsibility:
- Accept a parsed response body (dict) and a JSON Schema dict.
- Run jsonschema.validate() with clear, structured error output.
- NOT responsible for HTTP status, timing, or business logic.

Design note:
- Schemas live in schemas/endpoints/ as Python dicts (existing convention).
- This module does NOT load files from disk; callers import schema dicts directly.
- Keeps the validation call DRY and produces a consistent failure message.

Usage example:
    from schemas.endpoints.user.login_response import LOGIN_RESPONSE_DATA_SCHEMA
    from validators.schema_validator import validate_schema

    validate_schema(body, LOGIN_RESPONSE_DATA_SCHEMA)
"""

from typing import Any, Dict

from jsonschema import ValidationError, validate


def validate_schema(body: Any, schema: Dict[str, Any], context: str = "") -> None:
    """
    Validate *body* against *schema* using jsonschema.

    Args:
        body:    Parsed JSON response body (dict, list, or scalar).
        schema:  A JSON Schema dict (from schemas/endpoints/ or schemas/base/).
        context: Optional label for the error message, e.g. "POST /user/login".

    Raises:
        AssertionError: wrapping jsonschema.ValidationError with full path context.
    """
    try:
        validate(instance=body, schema=schema)
    except ValidationError as exc:
        path = " -> ".join(str(p) for p in exc.absolute_path) or "<root>"
        prefix = f"[{context}] " if context else ""
        raise AssertionError(
            f"{prefix}Schema validation failed at '{path}': {exc.message}\n"
            f"  Failed value : {exc.instance!r}\n"
            f"  Schema rule  : {exc.schema!r}"
        ) from exc
