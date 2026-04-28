from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from .base_client import BaseClient


class BookClient:
    """
    Domain client for book-related API operations.

    Encapsulates all HTTP calls to /book/* endpoints behind
    business-meaningful method signatures. Used by smoke, contract,
    reg_ci, and regression test suites.

    Note: search_by_page() uses 'curr' and 'limit' as query param names —
    these are the actual names the Spring Boot controller binds,
    not the Python method argument names (page_num / page_size).
    """

    def __init__(self, base_client: BaseClient) -> None:
        self._client = base_client

    def search_by_page(
        self,
        page_num: int = 1,
        page_size: int = 10,
        extra_params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        # Backend expects 'curr' for page number and 'limit' for page size.
        # These are the actual query param names the Spring Boot controller binds.
        params: Dict[str, Any] = {
            "curr": page_num,
            "limit": page_size,
        }
        if extra_params:
            params.update(extra_params)
        return self._client.get("/book/searchByPage", params=params, **kwargs)

    def query_detail(self, book_id: str, **kwargs: Any) -> requests.Response:
        return self._client.get(f"/book/queryBookDetail/{book_id}", **kwargs)

    def query_index_list(self, book_id: str, **kwargs: Any) -> requests.Response:
        return self._client.get(
            "/book/queryIndexList",
            params={"bookId": book_id},
            **kwargs,
        )

    def list_rank(
        self,
        type_: int = 1,
        **kwargs: Any,
    ) -> requests.Response:
        return self._client.get(
            "/book/listRank",
            params={"type": type_},
            **kwargs,
        )

    def list_categories(self, **kwargs: Any) -> requests.Response:
        return self._client.get("/book/listBookCategory", **kwargs)

    def list_comment_by_page(
        self,
        book_id: str,
        page_num: int = 1,
        page_size: int = 20,
        **kwargs: Any,
    ) -> requests.Response:
        """GET /book/listCommentByPage — params: bookId, pageNum, pageSize."""
        return self._client.get(
            "/book/listCommentByPage",
            params={"bookId": book_id, "pageNum": page_num, "pageSize": page_size},
            **kwargs,
        )

    def add_book_comment(self, book_id: str, content: str, **kwargs: Any) -> requests.Response:
        """POST /book/addBookComment — data: bookId, content."""
        return self._client.post(
            "/book/addBookComment",
            data={"bookId": book_id, "content": content},
            **kwargs,
        )

