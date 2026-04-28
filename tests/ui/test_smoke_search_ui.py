"""UI smoke test for the search feature.

Verifies that searching a known book title returns visible results.
No login required (search is a public feature).
"""
import pytest

from tests.ui.flows.search_flow import SearchFlow


@pytest.mark.ui
def test_smoke_search_ui(browser_page, base_url):
    """Searching a known title should display at least one result."""
    flow = SearchFlow(browser_page, base_url)
    flow.search_and_verify("斗破苍穹")
