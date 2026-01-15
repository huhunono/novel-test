"""
Book-related schemas for API contract validation.
Defines structures for both summary list items and detailed book information.
"""
from tests.schemas.common import is_int_like_Schema
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


"""
Schema definition for detailed book entities.
Used for validating responses from book information and detail endpoints.
"""
BOOK_DETAIL_SCHEMA ={
    "title":"Book Details",
    "description":"book detailed data used in list views ",
    "type": "object",
    "required":["id","catId","catName","bookName","authorId","authorName","bookDesc"],
    "properties":{
        "id":{
            "description":"Unique identifier for the book",
            "allOf": [is_int_like_Schema()]
        },
        "catId": {
            "description": "Unique identifier for the book category",
            "allOf": [is_int_like_Schema()]
        },
        "catName": {
            "description": "Book category names",
            "type": "string"
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
        },
        "bookDesc": {
            "description": "Book description information",
            "type": "string"
        }

    },
    "additionalProperties": True,

}