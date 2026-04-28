"""UI smoke test for the comment form on the book detail page.

Verifies that the comment textarea and submit button are visible,
and that the user can type into the comment box.

IMPORTANT: This test intentionally does NOT click 'Submit'.
Commenting is an irreversible state change (one comment per user
per book, no delete button on the page), so submitting would make
this test non-repeatable.
"""
import pytest

from tests.data.users import VALID_USER
from tests.ui.flows.comment_flow import BookCommentFlow


@pytest.mark.ui
def test_smoke_comment_form_ui(browser_page, base_url):
    """Log in, open a book detail, and verify the comment form works."""
    flow = BookCommentFlow(browser_page, base_url)
    flow.login_search_and_fill_comment(
        VALID_USER["username"],
        VALID_USER["password"],
        "斗破苍穹",
        "ui test comment draft",
    )
