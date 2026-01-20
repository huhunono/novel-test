LOGIN_DATA_SCHEMA = {
    "title": "login data ",
    "description": "represents succeed login data",
    "type": "object",
    "required": ["token"],
    "properties": {
        "token":{
            "type": "string",
        }
    },
}