"""UI smoke test for reading a book chapter.

Verifies the full path: search -> detail -> first chapter.
This is a read-only test with no state change.
Does not require login (chapters are publicly accessible).
"""
import pytest

from tests.ui.flows.read_chapter_flow import ReadChapterFlow


@pytest.mark.ui
def test_smoke_read_chapter_ui(browser_page, base_url):
    """Search a book, open its detail, and read the first chapter."""
    flow = ReadChapterFlow(browser_page, base_url)
    flow.read_first_chapter("斗破苍穹")
