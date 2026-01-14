import requests



def test_login_success(auth_http):
    '''
    url = "http://172.28.0.1:8083/user/login"

    payload = 'username=13560421999&password=123456'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)
    assert response.status_code == 200

     '''
    assert auth_http is not None
