from schemas.data.book.book_detail import BOOK_DETAIL_SCHEMA
from schemas.base.response import BASE_RESPONSE_SCHEMA

BOOK_RANK_ITEM_SCHEMA={
    **BASE_RESPONSE_SCHEMA,
    "title":"Book Rank",
    "description": "Contract schema for /book/listRank?type=..",
    "properties": {
        **BASE_RESPONSE_SCHEMA['properties'],
        "data":{
            "type": "array",
            "items": BOOK_DETAIL_SCHEMA
        }
    }


}