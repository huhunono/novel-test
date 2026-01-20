from schemas.common.primitives import is_int_like_Schema
BOOK_SHELF_SCHEMA={
    "title":"book shelf data",
    "description":"a list of books in book shelf",
    "type": "object",
    "required":["bookId","preContentId"],
    "properties": {
        "id": {"type": ["integer", "null"]},
        "userId": {"type": ["integer", "null"]},
        "bookId":{
            "allOf": [is_int_like_Schema()]
        },
        "preContentId":{
            "allOf": [is_int_like_Schema()]
        },
        "catName":{
            "type": "string"
        }
    },
    "additionalProperties": True,
}