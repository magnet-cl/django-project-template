# -*- coding: utf-8 -*-

# standard library
from os import environ
from os.path import dirname
from time import gmtime
from time import strftime
import sys

# fabric
from fabric.api import cd
from fabric.api import env
from fabric.api import get
from fabric.api import local
from fabric.api import prompt
from fabric.api import put
from fabric.api import run
from fabric.api import task
from fabric.colors import green
from fabric.colors import red
from fabric.context_managers import settings


# add django settings module to the import search path
sys.path.append(dirname(dirname(__file__)))
environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


@task
def get_db_data(root_dir=None, setting=''):
    """ Returns the name of the default database """
    if not root_dir:
        root_dir = env.server_root_dir
    with cd(root_dir):
        return run('python -Wi manage.py printdatabasedata {}'.format(setting))


@task
def migrate():
    """ Migrates database to the latest south migration """
    with cd(env.server_root_dir):
        run('python manage.py migrate')


@task
def backup_db():
    """ Backups database (postgreSQL). """
    # get database data
    db_name = get_db_data(setting='NAME')
    db_host = get_db_data(setting='HOST')
    db_user = get_db_data(setting='USER')

    # dumps folder creation
    dumps_folder = 'db_dumps/{}'.format(env.branch)
    cmd = 'mkdir -p {}'.format(dumps_folder)
    run(cmd)
    # generate backup file name based on its branch and current time
    dump_name = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    dump_name = '{}/{}.dump'.format(dumps_folder, dump_name)

    if db_host and db_user:
        cmd = 'pg_dump --host {} --username {} -Fc "{}" -f "{}"'.format(
            db_host, db_user, db_name, dump_name)
    else:
        cmd = 'pg_dump -Fc "{}" -f "{}"'.format(db_name, dump_name)
    run(cmd)

    return dump_name


@task
def download_db(compressed_file=None):
    """ Downloads the given compressed dump or generates it through
    `backup_db()` and downloads it. """

    if compressed_file is None:
        compressed_file = backup_db()

    # get returns a list, the first element is returned
    return get(compressed_file)[0]


@task
def import_db(dump_name=None):
    """ Imports a compressed database backup into the local system.
    In order to use this task, your local database engine must be postgreSQL.
    You can specify an sql dump file to use. If no file is supplied, then a
    copy of the production database is downloaded.

    Keyword arguments:
    dump_name -- The name of a sql dump of the database (default None)

    """
    if dump_name is None:
        dump_name = download_db()

    # get local database information
    local_engine = local(
        'python -Wi manage.py printdatabasedata ENGINE', capture=True)
    local_name = local(
        'python -Wi manage.py printdatabasedata NAME', capture=True)

    # check local database engine
    if local_engine != 'django.db.backends.postgresql':
        print(red('Please set your local database engine to postgreSQL.'))
        print(red('Aborting current task.'))
        return

    local('dropdb "{}"'.format(local_name))
    local('createdb "{}"'.format(local_name))
    local('pg_restore -d "{}" -O -j 2 "{}" --no-acl'.format(
        local_name, dump_name))

    print(green('Remember that there are settings established at DB level'))

    return dump_name


@task
def export_db(compressed_file=None):
    """ Exports the given compressed database backup into a staging server.

    If no compressed_file is given, then it is generated through
    `download_db()`.

    """

    if compressed_file is None:
        dump_name = download_db(compressed_file)
    else:
        dump_name = compressed_file

    # set host and branch for staging server
    staging_host = prompt(green('Type in the staging host: '))
    staging_branch = prompt(green('Type in the staging branch: '),
                            default='testing')
    staging_root_dir = env.server_root_dir
    if staging_branch != 'master':
        staging_root_dir = "{}-{}".format(staging_root_dir, staging_branch)

    # env.host replaced with staging host
    with settings(host_string=staging_host):
        print(green('get database name on destination sever'))
        db_name = get_db_data(root_dir=staging_root_dir, setting='NAME')

        print(green('Uploading file'))
        # upload the compressed file
        uploaded_dump = put(dump_name)[0]  # put returns a list

        run('dropdb "{}"'.format(db_name))
        run('createdb "{}"'.format(db_name))
        run('pg_restore -d "{}" -j 2 "{}" --no-acl'.format(
            db_name, uploaded_dump
        ))

        # cleanup files
        run('rm -f "{}"'.format(uploaded_dump))  # raw file

    print(green('Remember that there are settings established at DB level'))
