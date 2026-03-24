from jsonschema import validate
from schemas.endpoints.news.index_news_response import INDEX_NEWS_SCHEMA
import pytest
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract
def test_contract_list_index_news_schema(news_client):
    resp = news_client.list_index_news(timeout=10)
    body = assert_json_response(resp)

    validate(instance=body, schema=INDEX_NEWS_SCHEMA)
    assert body["ok"] is True and body["code"] == 200


