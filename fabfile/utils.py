from fabric.api import env
from fabric.api import prompt
from fabric.api import run

import sys


def git_clone(url, path):
    """ Utility method to clone git repositories. """
    cmd = 'git clone %s %s' % (url, path)
    run(cmd)


def git_checkout(branch):
    """ Utility method to change branches. """
    cmd = 'git checkout %s' % branch
    run(cmd)


def confirm_target(msg):
    host = prompt('Type in the host to confirm: ')
    branch = prompt('Type in the branch to confirm: ')

    if host == env.host and branch == env.branch:
        return True

    print 'Invalid host or branch.'
    sys.exit(1)
