from schemas.common.primitives import is_int_like_Schema

"""
Schema definition for a single Book Category entry.
Commonly used in dropdowns, navigation menus, and category list views.
"""

BOOK_CATEGORY_ITEM_SCHEMA = {
    "title": "Book Category Item",
    "type": "object",
    "required": ["id", "name"],
    "properties": {
        "id": {
            "description": "Category id (string/int-like)",
            **is_int_like_Schema(),
        },
        "name": {
            "description": "Category name",
            "type": "string",
        },
    },
    "additionalProperties": True,
}