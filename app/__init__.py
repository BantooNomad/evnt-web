# -*- coding: utf-8 -*-
__version__ = '0.1.0'

from flask import Flask
from flask import session, g
from flask import (render_template, url_for)
from flask import redirect, make_response, Flask
from flask import jsonify
from flask import abort, request
from json import dumps
from functools import wraps

import os
import logging
import hashlib
import uuid
from random import randint

app = Flask('app')
app.debug = True

import os

import rethinkdb as r
from rethinkdb import *
import psycopg2


import logging
logging.basicConfig(filename='TaskWangu.log', level=logging.DEBUG)
salt = 'd40037e1ff7841838235533d910bbf24'


RDB_HOST = os.environ.get('RDB_HOST') or '127.0.0.1'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
LINK_DB = 'LinkUs'


import requests
import simplejson

# conn_string = "host='188.226.195.158' dbname='LinkUs' user='synod' password='j633.125**//'"
# conn = psycopg2.connect(conn_string)
# cursor = conn.cursor()

ONLINE_LAST_MINUTES = 5

app.config[ONLINE_LAST_MINUTES] = 720
app.secret = 'I\xf9\x9cF\x1e\x04\xe6\xfaF\x8f\xe6)-\xa432'


def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(LINK_DB).run(connection)
        r.db(LINK_DB).table_create('User').run(connection)
        logging.info('Database setup completed')
    except RqlRuntimeError:
        logging.info('App database already exists')
    finally:
        connection.close()



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session[username] is None:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


"""
@app.before_request
def log_request():

    log_data = "LOG_INFO=" + simplejson.dumps(
    {
       'Request':'app.before',
    })
    requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", log_data)
"""


@app.before_request
def before_request():
    try:
        logging.info('before_request')
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=LINK_DB)
    except RqlDriverError:
        abort(503, "No database connection could be established")


@app.teardown_request
def teardown_request(exception):
    try:
        logging.info('teardown_request')
        g.rdb_conn.close()
    except AttributeError:
        pass

from userOps import *
from taskOps import *
