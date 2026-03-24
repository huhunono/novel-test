"""
tests/utils/assertions.py  —  COMPATIBILITY SHIM

This module re-exports all public assertion functions from validators/.
All existing imports across the test suite continue to work unchanged:

    from tests.utils.assertions import assert_json_response
    from tests.utils.assertions import assert_ok_true
    from tests.utils.assertions import assert_ok_false

Do NOT add new assertion logic here.
New assertions belong in validators/response_validator.py.
This file exists only to preserve backward-compatible import paths.
"""

from validators.response_validator import (  # noqa: F401  re-exported
    assert_json_response,
    assert_ok_false,
    assert_ok_true,
)

__all__ = [
    "assert_json_response",
    "assert_ok_true",
    "assert_ok_false",
]
