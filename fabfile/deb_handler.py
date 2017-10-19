from fabric.api import sudo
from fabric.api import task


@task
def install(package):
    """ Installs a deb package through apt-get. """

    print('Installing {}'.format(package))
    cmd = 'apt-get -y install %s' % (package)
    sudo(cmd)
