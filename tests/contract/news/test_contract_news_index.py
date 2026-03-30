import pytest

from schemas.endpoints.news.index_news_response import INDEX_NEWS_SCHEMA
from tests.utils.assertions import assert_json_response
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.contract


def test_contract_list_index_news_schema(news_client):
    resp = news_client.list_index_news(timeout=10)
    body = assert_json_response(resp)
    validate_schema(body, INDEX_NEWS_SCHEMA, context="GET /news/listIndexNews")
    assert body["ok"] is True and body["code"] == 200
