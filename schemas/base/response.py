"""
This module defines the common response contract (JSON Schema) for the API.
It is used for result validation in automated testing to ensure that the data structure returned by the backend interface meets expectations.
"""


BASE_RESPONSE_SCHEMA = {
    "title": "Base Response",
    "description": "System Response Format",
    "type": "object",
    "required": ["code", "data", "msg", "ok"],
    "properties": {
        "code": {
            "type": "integer",
            "description": "200 for success"
        },
        "data": {
            "description": "The actual response payload. Structure varies by endpoint.",
            "additionalProperties": True
        },
        "msg": {
            "type": "string",
            "description": "should return SUCCESS"
        },
        "ok": {
            "type": "boolean",
            "description": "Simplified flag for quick success/failure check"
        }
    },
    "additionalProperties": True
}