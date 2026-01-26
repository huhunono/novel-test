import requests

def assert_json_response(resp: requests.Response) -> dict:
    """
    Basic HTTP + JSON validation.
    No business logic included.
    """
    assert resp.status_code == 200, (
        f"status={resp.status_code}, text={resp.text[:300]}"
    )

    ct = resp.headers.get("content-type", "")
    assert "application/json" in ct, (
        f"non-json response: ct={ct}, text={resp.text[:300]}"
    )

    return resp.json()

def assert_ok_true(body: dict):
    assert body.get("ok") is True, body

def assert_ok_false(body: dict):
    assert body.get("ok") is False, body

