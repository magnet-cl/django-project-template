# standard library
from os import path

# fabric
from fabric.api import env
from fabric.api import task

# local and remote paths
env.local_root_dir = path.join(path.dirname(__file__), "..")
env.server_root_dir = 'example/path'

# server domain used by nginx
env.server_domain = 'example.com'

# git repositories
env.server_git_url = 'example/url.git'

# prefix used by configuration files
env.prefix = path.split(env.server_git_url)[1]  # split tail
env.prefix = path.splitext(env.prefix)[0]  # discard git suffix


@task
def set(address='default', user='magnet', branch='master', django_port='8000'):
    """ Address, user, branch and django port setter with shortcuts. """
    # host
    if address == 'default':
        env.hosts = ['example.com']
    else:
        # TODO Validate input
        env.hosts = [address]

    # user
    env.user = user

    # branch and django_port
    env.branch = branch
    env.django_port = django_port
    # if the branch is not master, append it to env.server_root_dir and set
    # django to run on a different port
    if env.branch != 'master':
        env.server_root_dir += '-%s' % env.branch
        env.django_port = int(env.django_port) + 1
