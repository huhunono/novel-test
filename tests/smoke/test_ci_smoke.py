from tests.utils.assertions import assert_json_response


def test_ci_smoke(base_client):
    """
    CI Smoke Test:
    Verify that the pipeline can successfully call a public API.
    """
    resp = base_client.get("/posts/1", timeout=10)

    body = assert_json_response(resp)

    assert body["id"] == 1