from schemas.common.primitives import is_int_like_Schema
USERINFO_DATA_SCHEMA = {
    "title": "user info data ",
    "description": "user info after login",
    "type": "object",
    "required": ["username"],
    "properties": {
        "id": {"type": ["integer", "null"]},
        "username": {
            "title": "user username",
            "type": "string"
        },
        "nickName": {
            "title": "user nickName",
            "type": "string"
        },
        "accountBalance": {
            "title": "user accountBalance",
            "allOf": [is_int_like_Schema()]
        },
        "userSex":{
            "title": "user gender",
            "allOf": [is_int_like_Schema()]
        }
    },
    "additionalProperties": True,
}