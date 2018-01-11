from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    verbose_name = _('users')
    name = 'users'
