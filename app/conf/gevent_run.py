#!/usr/bin/env python
# -*- coding: utf-8 -
import os
import sys
from subprocess import call


print 'OS Name', os.name
print 'Platform', sys.platform
print 'Parent PID -->', os.getppid()
print 'Process ID -->', os.getpid()

if (os.name == 'posix'):
    print 'Kernel Version -->', os.system('uname -r')
else:
    pass

# gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker module:app
# run2 = 'gunicorn -w 4 -b 127.0.0.1:4000 myproject:app -k gevent'
# run = 'gunicorn -w 4 flask_render:app -k gevent'
# call(['ls', '-l'])
# call(['gunicorn', 'flask_render:app', '-k', 'gevent'])
# |>>
# gunicorn options --graceful-time --keep-alive --max-connects --concurrency
# --debug=True --loglevel=INFO --loglevel=ERROR --loglevel=CRITICAL
# Best way --> use this
# gunicorn -c gunicorn-config.py flask_render:app -k gevent
# -c option for config file
call(['gunicorn', '-w', '4', 'flask_render:app', '-k', 'gevent_wsgi'])

#from commands import *
