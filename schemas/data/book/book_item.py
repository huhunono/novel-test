from schemas.common.primitives import is_int_like_Schema
BOOK_ITEM_SCHEMA ={
    "title":"Book Item Summary",
    "description":"book data used in list views and search results",
    "type": "object",
    "required":["id","bookName","authorId","authorName"],
    "properties":{
        "id":{
            "description":"Unique identifier for the book",
            "allOf": [is_int_like_Schema()]
        },
        "bookName": {
                "description": "Full title of the book entity",
                "type": "string"
        },
        "authorId": {
                "description": "Identifier for the author, supporting string/int for flexibility",
                "allOf": [is_int_like_Schema()]
        },
        "authorName": {
                "description": "Display name of the book's creator",
                "type": "string"
        }
    },
    "additionalProperties": True,
}