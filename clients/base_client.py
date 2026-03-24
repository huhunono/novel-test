from __future__ import annotations

from typing import Mapping, Optional, Any

import requests


class BaseClient:
    """
    Thin wrapper around requests.Session.

    - Accepts a base_url.
    - Supports default headers.
    - Exposes get/post/put/patch/delete.
    - Returns raw requests.Response objects.
    """

    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Mapping[str, str]] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = (base_url or "").rstrip("/")
        self._session = session or requests.Session()

        if default_headers:
            self._session.headers.update(default_headers)

    @property
    def session(self) -> requests.Session:
        return self._session

    @property
    def headers(self) -> Mapping[str, str]:
        return self._session.headers

    def close(self) -> None:
        self._session.close()

    def _make_url(self, url: str) -> str:
        # Allow both absolute URLs and relative paths.
        if url.startswith("http://") or url.startswith("https://"):
            return url

        if not self.base_url:
            return url

        if url.startswith("/"):
            return f"{self.base_url}{url}"

        return f"{self.base_url.rstrip('/')}/{url}"

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        return self._session.get(self._make_url(url), **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        return self._session.post(self._make_url(url), **kwargs)

    def put(self, url: str, **kwargs: Any) -> requests.Response:
        return self._session.put(self._make_url(url), **kwargs)

    def patch(self, url: str, **kwargs: Any) -> requests.Response:
        return self._session.patch(self._make_url(url), **kwargs)

    def delete(self, url: str, **kwargs: Any) -> requests.Response:
        return self._session.delete(self._make_url(url), **kwargs)

