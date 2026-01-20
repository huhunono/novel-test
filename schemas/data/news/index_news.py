from schemas.common.primitives import is_int_like_Schema

"""
Used in ndex_news_response.py to validate the list of news.
"""

NEWS_INDEX_SCHEMA = {

    "title": "NEWS index list",
    "description": "Represents a single news entry metadata used for homepage news lists.",
    "type": "object",
    "required": ["title","id","sourceName","catId","catName"],
    "properties": {
        "title": {
            "description":"title of the news",
            "type": "string"
        },
        "id":{
            "description":"unique id of a single news",
            "allOf": [is_int_like_Schema()]
        },
        "sourceName": {
            "description": "The name of the publishing source or platform.",
            "type": ["string", "null"]
        },
        "catId": {
            "description": "The category ID the news belongs to (e.g., Politics, Tech).",
            "allOf": [is_int_like_Schema()]
        },
        "catName": {
            "description": "The human-readable name of the category.",
            "type": "string"
        },
    },
    "additionalProperties": True,
}