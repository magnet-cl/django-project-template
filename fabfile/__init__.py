import config
import db
import gunicorn
import nginx
import project
import utils

assert config
assert db
assert gunicorn
assert nginx
assert project
assert utils

# fabric global configuration
from fabric.api import env
from os import path

# support ssh_config
ssh_config_file = '{}/.ssh/config'.format(path.expanduser('~'))
if path.isfile(ssh_config_file):
    env.use_ssh_config = True
