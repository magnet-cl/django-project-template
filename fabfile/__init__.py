from . import config
from . import db
from . import gunicorn
from . import nginx
from . import project
from . import utils

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
