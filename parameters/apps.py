from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ParametersConfig(AppConfig):
    name = 'parameters'
    verbose_name = _('parameters')
