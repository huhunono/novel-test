from schemas.data.user.list_book_shelf import BOOK_SHELF_SCHEMA
from schemas.base.response import BASE_RESPONSE_SCHEMA
from schemas.common.pagination import pagination_schema

BOOK_SHELF_RESPONSE_SCHEMA={
    **BASE_RESPONSE_SCHEMA,
    "title": "user book shelf",
    "description": "Contract schema for /user/listBookShelfByPage",
    "properties": {
        **BASE_RESPONSE_SCHEMA['properties'],
        "data": pagination_schema(BOOK_SHELF_SCHEMA)
    }

}