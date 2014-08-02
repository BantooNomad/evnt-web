import os

secret = os.urandom(24)


DEBUG=True
SECRET_KEY=secret
CSRF_ENABLED=True
CSRF_SESSION_LKEY='dev_key_h8asSNJ9s9=+'
THREADED = False
