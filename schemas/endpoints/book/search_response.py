from schemas.base.response import BASE_RESPONSE_SCHEMA
from schemas.common.pagination import pagination_schema
from schemas.data.book.book_item import BOOK_ITEM_SCHEMA

SEARCH_BOOK_RESPONSE_SCHEMA={
    **BASE_RESPONSE_SCHEMA,
    "title": "search book response",
    "description": "Contract schema for /book/searchByPage?keyword=...",
    "properties": {
        **BASE_RESPONSE_SCHEMA["properties"],
        "data":pagination_schema(BOOK_ITEM_SCHEMA),
    },
}