'''
This .py file is used to test the response of bento service container from inside the flask-app container.

'''

import requests

response = requests.get('http://bento-service:3000')
print(response.status_code)
print(response.text)