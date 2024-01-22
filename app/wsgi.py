'''
Importing my flask 'app' as application to be used in the uwsgi.ini file for uwsgi config.

'''
## Checking sys path
import sys
print(sys.path)
from app import app as application
