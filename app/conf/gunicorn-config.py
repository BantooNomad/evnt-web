#!/usr/bin/env python

import os

import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1


def numCPUs():
    if not hasattr(os, 'sysconf'):
        raise RuntimeError('No sysconf detected.')
    return os.sysconf('SC_NPROCESSORS_ONLN')


use = 'flask_render:app'
bind = '0.0.0.0:8000'
workers = numCPUs() * 2 + 1
# backlog = 2048
# worker_class = 'sync'
worker_class = 'gevent'
preload = True
debug = True
# timeout = 60
graceful_timeout = 30
proc_name = 'gunicorn-flask'
proxy_protocol = False
daemon = True
# spew = True
worker_connections = 1000
accesslog = '/tmp/gunicorn-access.log'
keepalive = 2
access_log_format = '"%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
limit_request_fields = 100
max_requests = 1000
errorlog = '/tmp/gunicorn.log'
pidfile = '/tmp/gunicorn.pid'
logfile = '/tmp/gunicorn.log'
