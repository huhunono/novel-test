from __future__ import annotations

from typing import Any, Dict

import requests

from .base_client import BaseClient


class UserClient:
    """
    Higher-level user-related API operations.

    Currently unused by tests but provided for future refactors.
    """

    def __init__(self, base_client: BaseClient) -> None:
        self._client = base_client

    def login(self, username: str, password: str, **kwargs: Any) -> requests.Response:
        data: Dict[str, Any] = {"username": username, "password": password}
        return self._client.post("/user/login", data=data, **kwargs)

    def user_info(self, **kwargs: Any) -> requests.Response:
        return self._client.get("/user/userInfo", **kwargs)

    def refresh_token(self, **kwargs: Any) -> requests.Response:
        """POST /user/refreshToken — requires Authorization header (e.g. from session)."""
        return self._client.post("/user/refreshToken", **kwargs)

    def add_to_bookshelf(self, book_id: str, **kwargs: Any) -> requests.Response:
        return self._client.post(
            "/user/addToBookShelf",
            data={"bookId": book_id},
            **kwargs,
        )

    def remove_from_bookshelf(self, book_id: str, **kwargs: Any) -> requests.Response:
        return self._client.delete(
            f"/user/removeFromBookShelf/{book_id}",
            **kwargs,
        )

    def query_in_shelf(self, book_id: str, **kwargs: Any) -> requests.Response:
        return self._client.get(
            "/user/queryIsInShelf",
            params={"bookId": book_id},
            **kwargs,
        )

    def list_bookshelf_by_page(
        self,
        page_num: int = 1,
        page_size: int = 20,
        **kwargs: Any,
    ) -> requests.Response:
        return self._client.get(
            "/user/listBookShelfByPage",
            params={"pageNum": page_num, "pageSize": page_size},
            **kwargs,
        )

