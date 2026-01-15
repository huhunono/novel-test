"""
Pagination Schema Module
Provides a reusable factory function for paged data validation.
"""
from tests.schemas.common import is_int_like_Schema
def pagination_schema(item_schema):
    """
        Generates a schema for paginated data objects.

        Args:
            item_schema (dict): The JSON schema definition for a single item
                               inside the 'list' array.

        Returns:
            dict: A complete JSON schema for a paginated data structure.
        """
    return {
        "title": "Pagination Wrapper",
        "description": "Standard structure for paginated response data",
        "type": "object",
        "required": ["pageNum","pageSize","total","list","pages"],
        "properties": {
            "pageNum":{
                "description": "Current page number (1-based index)",
                "allOf": [is_int_like_Schema()]
            },
            "pageSize":{
                "description": "Number of items per page",
                "allOf": [is_int_like_Schema()]
            },
            "total":{
                "description": "Total count of records across all pages",
                "allOf": [is_int_like_Schema()]
            },
            "pages": {
                "description": "Total number of pages",
                "allOf": [is_int_like_Schema()]
            },
            "list":{
                "description": "Array of business objects for the current page",
                "type": "array",
                "items": item_schema,
            },
        },
        "additionalProperties": True,
    }