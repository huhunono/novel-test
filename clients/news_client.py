from __future__ import annotations

from typing import Any

import requests

from .base_client import BaseClient


class NewsClient:
    """
    Higher-level news-related API operations.
    """

    def __init__(self, base_client: BaseClient) -> None:
        self._client = base_client

    def list_index_news(self, **kwargs: Any) -> requests.Response:
        """GET /news/listIndexNews."""
        return self._client.get("/news/listIndexNews", **kwargs)
