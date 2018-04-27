from fabric.api import run
from fabric.api import task

from .service import memcached_handler

# standard library
from re import search


@task
def install():
    """ Installs memcache. """
    run('sudo apt-get update')
    run('sudo apt-get -y install memcached')
    run('sudo apt-get -y install libmemcached-tools')

    # create logs directory
    cmd = 'mkdir -p logs'
    run(cmd)


@task
def start():
    """ Starts the memcached service. """
    memcached_handler('start')


@task
def stop():
    """ Stops the memcached service. """
    if search('running', memcached_handler('status')):
        memcached_handler('stop')


@task
def restart():
    """ Restarts the memcached service. """
    memcached_handler('restart')
