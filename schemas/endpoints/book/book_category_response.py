from schemas.base.response import BASE_RESPONSE_SCHEMA
from schemas.data.book.category_item import BOOK_CATEGORY_ITEM_SCHEMA

BOOK_CATEGORY_RESPONSE_SCHEMA = {
    **BASE_RESPONSE_SCHEMA,
    "title": "Book Category Response",
    "description": "Contract schema for /book/category",
    "properties": {
        **BASE_RESPONSE_SCHEMA["properties"],
        "data":{
            "type": "array",
            "items": BOOK_CATEGORY_ITEM_SCHEMA,
        },
    },
}
