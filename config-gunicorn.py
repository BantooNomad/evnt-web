#!/usr/bin/env python

import os

def numCPUs():
    if not hasattr(os, 'sysconf'):
        raise RuntimeError('No sysconf detected.')
    return os.sysconf('SC_NPROCESSORS_ONLN')


bind = '127.0.0.1:8000'
workers = 4
worker_class = 'gevent'
debug = True
daemon = True
pidfile = '/tmp/gunicorn.pid'
logfile = '/tmp/gunicorn.log'
