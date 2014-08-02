#!/usr/bin/env python

import os

def numCPUs():
    if not hasattr(os, 'sysconf'):
        raise RuntimeError('No sysconf detected.')
    return os.sysconf('SC_NPROCESSORS_ONLN')


bind = '0.0.0.0:8001'
workers = 4
# backlog = 2048
# worker_class = 'sync'
worker_class = 'gevent'
debug = True
daemon = True
pidfile = '/tmp/gunicorn.pid'
logfile = '/tmp/gunicorn.log'

# gunicorn -c config-gunicorn.py views:app
