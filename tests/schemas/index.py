"""
Schema for a single chapter/index entry within a book's table of contents.
Used primarily for validating chapter lists and navigation menus.
"""
from tests.schemas.common import is_int_like_Schema
BOOK_INDEX_SCHEMA = {
    "title": "Book Index Item",
    "description": "Represents metadata for an individual chapter or volume index.",
    "type": "object",
    "required": ["id","bookId","indexNum","indexName"],
    "properties": {
        "id":{
            "description": "Unique identifier for the chapter (supports string or integer IDs).",
            "allOf": [is_int_like_Schema()]
        },
        "bookId":{
            "description":"Unique identifier for the book",
            "allOf": [is_int_like_Schema()]
        },
        "indexNum":{
            "description": "The sequential order of the chapter (e.g., Chapter 1, 2, 3).",
            "allOf": [is_int_like_Schema()]
        },
        "isVip":{
            "description": "Subscription status: 0 for free content, 1 for premium content.",
            "allOf": [is_int_like_Schema()]
        },
    },
    "additionalProperties": True,
}

