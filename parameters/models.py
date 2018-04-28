# -*- coding: utf-8 -*-
""" Models for the parameters application. """
#  standard library
import json
import datetime
import time

# django
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel
from parameters.enums import ParameterDefinitionList
from django.core.cache import cache


class Parameter(BaseModel):
    raw_value = models.TextField(
        verbose_name=_("value"),
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_("name"),
        choices=ParameterDefinitionList.choices,
        unique=True,
    )
    kind = models.CharField(
        max_length=255,
        verbose_name=_("kind"),
        choices=(
            ('int', _('integer')),
            ('str', _('text')),
            ('time', _('time')),
            ('json', _('json')),
        )
    )
    cache_seconds = models.PositiveIntegerField(
        verbose_name=_("cache seconds"),
        default=3600,
    )

    def clean(self):
        if self.kind == 'int':
            try:
                int(self.raw_value)
            except ValueError:
                raise ValidationError(_('Invalid input'))

        if self.kind == 'time':
            try:
                time.strptime(self.raw_value, '%H:%M')
            except ValueError:
                raise ValidationError(_('Invalid time format'))

    @property
    def value(self):
        if self.kind == 'int':
            return int(self.raw_value)

        if self.kind == 'json':
            return json.loads(self.raw_value)

        if self.kind == 'time':
            hour = int(self.raw_value.split(':')[0])
            minute = int(self.raw_value.split(':')[1])
            return datetime.time(hour, minute)

        return self.raw_value

    @value.setter
    def value(self, value):
        self.raw_value = value

    @classmethod
    def value_for(cls, name):
        cache_key = 'parameters-{}'.format(name)
        cached_parameter = cache.get(cache_key)

        if cached_parameter:
            raw_value, kind = json.loads(cached_parameter)
            parameter = Parameter.objects.get(
                raw_value=raw_value,
                kind=kind,
            )

        try:
            parameter = Parameter.objects.get(
                name=name
            )
        except Parameter.DoesNotExist:
            for parameter_definition in ParameterDefinitionList.definitions:
                if parameter_definition.name == name:
                    parameter = Parameter.objects.create(
                        name=name,
                        kind=parameter_definition.kind,
                        raw_value=parameter_definition.default,
                    )

        cache.set(
            cache_key,
            json.dumps([parameter.raw_value, parameter.kind]),
            parameter.cache_seconds  # the time in seconds to store the value
        )

        return parameter.value
