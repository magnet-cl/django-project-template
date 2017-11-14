from fabric.api import cd
from fabric.api import env
from fabric.api import get
from fabric.api import local
from fabric.api import prompt
from fabric.api import put
from fabric.api import run
from fabric.api import task
from fabric.colors import green
from fabric.context_managers import settings

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

    print('Invalid host or branch.')
    sys.exit(1)


@task
def backup_media(relative_path=''):
    """
    Backups media folder.

    kwargs:
        relative_path: a relative folder on the MEDIA folder
    """
    # local django settings
    with cd(env.server_root_dir):
        full_path = ' project/media/{}'.format(
            relative_path
        )

        backup_name = 'media.tar.gz'

        cmd = 'tar -cv {} | gzip > {}'.format(full_path, backup_name)
        print(green('Generating media backup'))
        run(cmd)

    return backup_name


@task
def download_media(backup_name=None, relative_path=''):
    """ Downloads the given compressed media or generates it through
    `backup_media()` and downloads it. """

    if backup_name is None:
        backup_name = backup_media(relative_path)

    with cd(env.server_root_dir):
        # get returns a list, the first element is returned
        print(green('Downloading media backup'))
        return get(backup_name)[0]


@task
def export_media(backup_name=None, relative_path=''):
    """ Backups media folder, downloads it, and loads it on another server """
    if backup_name is None:
        backup_name = download_media(relative_path=relative_path)

    # set host and branch for staging server
    staging_host = prompt(green('Type in the staging host: '))
    staging_branch = prompt(
        green('Type in the staging branch: '),
        default='testing'
    )

    staging_root_dir = env.server_root_dir
    if staging_branch != 'master':
        staging_root_dir = "{}-{}".format(staging_root_dir, staging_branch)

    staging_root_dir = env.server_root_dir

    # env.host replaced with staging host
    with settings(host_string=staging_host):
        print(green('Uploading file'))
        uploaded_dump = put(backup_name)[0]  # put returns a list

        run('mv {} {}'.format(uploaded_dump, env.server_root_dir))

        # upload the compressed file
        with cd(env.server_root_dir):
            run('tar -zxvf {}'.format(uploaded_dump))

            # cleanup files
            run('rm -f "{}"'.format(uploaded_dump))  # raw file


@task
def import_media(backup_name=None, relative_path=''):
    """ Backups media folder, downloads it, and loads it this computer """
    if backup_name is None:
        backup_name = download_media(relative_path=relative_path)

    # upload the compressed file
    print(green('Uncompressing media backup'))
    local('tar -zxvf {} -C .'.format(backup_name))
