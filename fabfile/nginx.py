from fabric.api import cd
from fabric.api import env
from fabric.api import sudo
from fabric.api import task
from fabric.contrib.files import upload_template

from . import deb_handler
from .service import nginx_handler


@task
def install():
    """ Installs nginx through deb_handler. """
    deb_handler.install('nginx')


@task
def start():
    """ Starts the nginx service. """
    nginx_handler('start')


@task
def stop():
    """ Stops the nginx service. """
    nginx_handler('stop')


@task
def restart():
    """ Restarts the nginx service. """
    nginx_handler('restart')


def add_site(filename, context):
    """ Deploys a new nginx configuration site. """
    destination = '/etc/nginx/sites-available/{}-{}'.format(
        env.prefix, env.branch)
    upload_template(filename, destination, context=context, use_sudo=True)

    # set root as file owner
    cmd = 'chown root:root {}'.format(destination)
    sudo(cmd)


@task
def add_django_site():
    """ Deploys a nginx configuration site for django. """
    context = {
        'domain': env.server_domain,
        'server_root_dir': env.server_root_dir,
        'proxy_port': env.django_port
    }
    filename = '%s/fabfile/templates/nginx_site.conf'
    filename %= env.local_root_dir

    add_site(filename, context)

    # enable site configuration
    with cd('/etc/nginx/sites-enabled'):
        cmd = 'ln -s -f /etc/nginx/sites-available/{}-{} .'.format(
            env.prefix, env.branch)
        sudo(cmd)
