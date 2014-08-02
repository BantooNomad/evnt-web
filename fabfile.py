from fabric.api import *

env.user = 'root'
env.hosts = ['188.226.195.158']


def gunicorn():
    with cd('/tmp/evnt-web/evnt'):
        run('gunicorn -c config-gunicorn.py app:app')


def moveSupervisor():
    put('supervisord.conf')


def supervisor():
    with cd('/tmp/evnt-web/evnt'):
        run('supervisord start evnt-web')


def setup_server():
    run('pty=False')
    run('mkdir /tmp/evnt-web')
    with cd('/tmp/evnt-web'):
        run('git clone https://github.com/nailab/linkus.git')
        with cd('/tmp/evnt-web/evnt'):
            result = run('pip install -r requirements.txt && gunicorn -c config-gunicorn.py app:app')
            if result.failed:
                local('GUNICORN failed')

            run('gunicorn -c config-gunicorn.py app:app')
            prepare_deploy()


def clean():
    run('rm -r /tmp/evnt-web')
    run('rm -r /tmp/evnt-web/evnt')
    run('apt-get clean && apt-get dist-upgrade')
    local('server cleaned up ...')


def installDeps():
    run('apt-get install redis')
    run('apt-get install postgresql9.3')
    run('apt-get install rethinkdb')


def prepare_deploy():
    run("apt-get update && apt-get -y dist-upgrade")


def restartNginx():
    run('service nginx restart')


def deploy():
    setup_server()
    moveSupervisor()
    supervisor()
    # restartNginx()
