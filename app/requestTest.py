import requests

response = requests.get('http://bento-service:3000')
print(response.status_code)
print(response.text)