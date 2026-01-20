from schemas.base.response import BASE_RESPONSE_SCHEMA
from schemas.common.pagination import pagination_schema
from schemas.data.book.index_item import BOOK_INDEX_SCHEMA

QUERY_INDEX_LIST_RESPONSE_SCHEMA ={
    **BASE_RESPONSE_SCHEMA,
    "title": "Query Index List Response",
    "description": "Contract schema for /book/queryIndexList?bookId=...",
    "properties": {
        **BASE_RESPONSE_SCHEMA["properties"],
        "data": pagination_schema(BOOK_INDEX_SCHEMA),
    },
}