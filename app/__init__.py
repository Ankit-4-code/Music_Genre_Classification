'''
## This is used for development of flask app and to test out the connection with the bentoml container.
## This method of Flask app initialization had to be changed and finally an app.py has been used in it's place since uwsgi has a bug with the app module import.

from flask import Flask

app = Flask(__name__)

from . import routes

'''