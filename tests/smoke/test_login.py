import requests



def test_login_success(auth_http):
    """
        Smoke Test: Verify Successful Authentication.

        This test ensures that the login credentials provided in the configuration
        are valid and the 'auth_http' fixture can successfully establish a session.
        It is a prerequisite for all subsequent authenticated API calls.
    """
    assert auth_http is not None
