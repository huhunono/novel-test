from schemas.data.user.login import LOGIN_DATA_SCHEMA
from schemas.base.response import BASE_RESPONSE_SCHEMA

LOGIN_RESPONSE_DATA_SCHEMA={
    **BASE_RESPONSE_SCHEMA,
        "title": "Login Response",
        "description": "Contract schema for /user/login",
        "properties": {
            **BASE_RESPONSE_SCHEMA["properties"],
            "data":LOGIN_DATA_SCHEMA,
    },
}
