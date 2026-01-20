import requests
from jsonschema import validate
from schemas.endpoints.news.index_news_response import INDEX_NEWS_SCHEMA
import pytest

pytestmark = pytest.mark.contract
def test_contract_list_index_news_schema(base_url):
    resp = requests.get(base_url + "/news/listIndexNews")
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")

    body = resp.json()

    validate(instance=body, schema=INDEX_NEWS_SCHEMA)
    assert body["ok"] is True and body["code"] == 200


