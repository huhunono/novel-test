"""
Book-related schemas for API contract validation.
Defines structures for both summary list items and detailed book information.
"""
from schemas.common.primitives import is_int_like_Schema
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
