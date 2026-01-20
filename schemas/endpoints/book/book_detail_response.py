from schemas.base.response import BASE_RESPONSE_SCHEMA
from schemas.data.book.book_detail import BOOK_DETAIL_SCHEMA

QUERY_BOOK_DETAIL_RESPONSE_SCHEMA = {
    **BASE_RESPONSE_SCHEMA,
    "title": "Query Book Detail Response",
    "description": "Contract schema for /book/queryBookDetail/{bookId}",
    "properties": {
        **BASE_RESPONSE_SCHEMA["properties"],
        "data": BOOK_DETAIL_SCHEMA,

    },
}