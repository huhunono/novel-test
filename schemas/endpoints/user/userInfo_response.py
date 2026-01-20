from schemas.base.response import BASE_RESPONSE_SCHEMA
from schemas.data.user.userInfo import USERINFO_DATA_SCHEMA

USERINFO_RESPONSE={
    **BASE_RESPONSE_SCHEMA,
    "title": "user info response",
    "description": "Contract schema for /user/userInfo",
    "properties": {
        **BASE_RESPONSE_SCHEMA["properties"],
        "data": USERINFO_DATA_SCHEMA,
    },
}