import requests
from jsonschema import validate
from schemas.endpoints.news.index_news_response import INDEX_NEWS_SCHEMA
import pytest
from tests.utils.assertions import assert_json_response

pytestmark = pytest.mark.contract
def test_contract_list_index_news_schema(base_url,plain_http):
    resp = plain_http.get(base_url + "/news/listIndexNews",timeout=10)
    body = assert_json_response(resp)

    validate(instance=body, schema=INDEX_NEWS_SCHEMA)
    assert body["ok"] is True and body["code"] == 200


