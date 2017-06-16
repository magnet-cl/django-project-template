from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import run
from fabric.api import task
from fabric.contrib.files import upload_template

from service import add_systemd_service
from service import gunicorn_handler

# standard library
from re import search


@task
def install():
    """ Installs gunicorn. """
    with cd(env.server_root_dir):
        with prefix('. .env/bin/activate'):
            run('pip install gunicorn')

    # create logs directory
    cmd = 'mkdir -p logs'
    run(cmd)


@task
def start():
    """ Starts the gunicorn service. """
    gunicorn_handler('start')


@task
def stop():
    """ Stops the gunicorn service. """
    if search('running', gunicorn_handler('status')):
        gunicorn_handler('stop')


@task
def restart():
    """ Restarts the gunicorn service. """
    gunicorn_handler('restart')


def add_gunicorn_conf():
    """ Deploys the gunicorn configuration file. """
    filename = '{}/fabfile/templates/gunicorn.conf'
    filename = filename.format(env.local_root_dir)
    destination = '{}/gunicorn_conf.py'.format(env.server_root_dir)
    context = {
        'user': env.user,
        'server_root_dir': env.server_root_dir,
        'django_port': env.django_port
    }
    upload_template(filename, destination, context=context)


@task
def add_gunicorn_service():
    """ Deploys an upstart service for gunicorn. """

    # deploys the gunicorn config file
    add_gunicorn_conf()

    filename = '{}/fabfile/templates/gunicorn_systemd.service'
    filename = filename.format(env.local_root_dir)

    context = {
        'prefix': env.prefix,
        'server_root_dir': env.server_root_dir,
        'user': env.user,
    }

    add_systemd_service(filename, context)
