from fabric.api import task, sudo

def install(package):
    """ Installs a deb package through apt-get. """

    print 'Installing %s' % (package)
    cmd = 'apt-get -y install %s' % (package)
    sudo(cmd)
