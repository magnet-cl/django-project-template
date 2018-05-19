# -*- coding: utf-8 -*-

# standard library
import collections

# django
from django.utils.translation import ugettext_lazy as _

ParameterDefinition = collections.namedtuple(
    'Parameter',
    [
        'name',
        'default',
        'kind',
        'verbose_name',
    ]
)


class ParameterDefinitionList(object):
    definitions = [
        ParameterDefinition(
            name='DEFAULT_URL_PROTOCOL',
            default='https',
            kind='str',
            verbose_name=_('Default url protocol'),
        ),
    ]

    choices = tuple((x.name, x.verbose_name) for x in definitions)
