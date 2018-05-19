# -*- coding: utf-8 -*-
""" Models for the parameters application. """
#  standard library
import json
import datetime
import time

# django
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
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
            ('date', _('date')),
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

        if self.kind == 'date':
            try:
                datetime.datetime.strptime(self.raw_value, '%Y-%m-%d')
            except ValueError:
                raise ValidationError(_('Invalid time format'))

    @property
    def value(self):
        if self.kind == 'int':
            return int(self.raw_value)

        if self.kind == 'json':
            return json.loads(self.raw_value)

        if self.kind == 'time':
            return time.strptime(self.raw_value, '%H:%M')

        if self.kind == 'date':
            return datetime.datetime.strptime(self.raw_value, '%Y-%m-%d')

        return self.raw_value

    @value.setter
    def value(self, value):
        self.raw_value = value

    @classmethod
    def cache_key(cls, name):
        return 'parameters-{}'.format(slugify(name))

    @classmethod
    def value_for(cls, name):
        cache_key = cls.cache_key(name)

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

        parameter.store_in_cache()

        return parameter.value

    # django methods
    def save(self, *args, **kwargs):
        self.store_in_cache()
        super(Parameter, self).save(*args, **kwargs)

    # public methods
    def store_in_cache(self):
        cache_key = Parameter.cache_key(self.name)

        cache.set(
            cache_key,
            json.dumps([self.raw_value, self.kind]),
            self.cache_seconds  # the time in seconds to store the value
        )
