from schemas.base.response import BASE_RESPONSE_SCHEMA
from schemas.data.news.index_news import NEWS_INDEX_SCHEMA

INDEX_NEWS_SCHEMA={
    **BASE_RESPONSE_SCHEMA,
    "title": "news index response",
    "description": "Contract schema for /news/listIndexNews",
    "properties": {
        **BASE_RESPONSE_SCHEMA["properties"],
        "data":{
            "type": "array",
            "items": NEWS_INDEX_SCHEMA
        }
    },
}