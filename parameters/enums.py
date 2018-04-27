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
            name='DEFAULT_PROTOCOL',
            default='https',
            kind='str',
            verbose_name=_('default protocol: https'),
        ),
    ]

    choices = tuple((x.name, x.verbose_name) for x in definitions)
