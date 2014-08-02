import os

secret = os.urandom(24)


DEBUG=True
SECRET_KEY=secret
CSRF_ENABLED=True
CSRF_SESSION_LKEY='dev_key_h8asSNJ9s9=+'
THREADED = False

CLIENT_ID = '20567748533.apps.googleusercontent.com'
CLIENT_SECRET = '82Y0LzHkrfXlep81sVLWIWh2'
SCOPE = 'https://medtest21.appspot.com/oauth2callback'
