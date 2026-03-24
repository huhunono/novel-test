"""Stable book ID constants shared across test suites.

Only include IDs that are:
- High-frequency (appear in 2+ test files)
- Semantically clear
- Expected to remain stable in the test environment
"""

# A known valid book used for detail / index-list / in-shelf queries.
# Appears in: smoke/book, contract/book, reg_ci/book, contract/user
BOOK_ID_DETAIL: int = 2010824442059300864

# A known valid book used for bookshelf add/remove flow tests.
# Appears in: regression/user/test_reg_bookshelf_add_remove_flow,
#             regression/user/test_reg_bookshelf_security
BOOK_ID_SHELF_FLOW: str = "2014580673134784512"

# A known valid book used for the reg_ci bookshelf minimal flow test.
# Appears in: reg_ci/user/test_user_bookshelf_ci
BOOK_ID_SHELF_CI: str = "2010826914387599360"

# A known valid book used for the idempotency add-to-shelf test.
# Appears in: regression/user/test_reg_addToBookShelf_idempotent
BOOK_ID_IDEMPOTENT: str = "2014580046711287808"
