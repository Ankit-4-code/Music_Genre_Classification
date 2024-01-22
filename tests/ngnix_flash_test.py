'''
This is to ping the aws ec2 instance and get a response.
'''


import requests

def test_nginx_to_flask():
    url = "http://3.92.186.169/" ## aws ec2 public url
    response = requests.get(url)

    assert response.status_code == 200
    assert "expected content in response" in response.text

if __name__ == "__main__":
    test_nginx_to_flask()