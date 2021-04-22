# -*- coding: utf-8 -*-
""" Models for the parameters application. """
#  standard library
import json
import datetime
import time

# django
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel

# enums
from parameters.enums import ParameterDefinitionList


class Parameter(BaseModel):
    raw_value = models.TextField(
        verbose_name=_("value"),
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_("name"),
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

        self.run_validators()

    def run_validators(self):
        parameter_definition = ParameterDefinitionList.get_definition(
            self.name
        )
        value = self.value
        for validator in parameter_definition.validators:
            validator(value)

    @property
    def value(self):
        return self.__class__.process_value(self.kind, self.raw_value)

    @classmethod
    def process_value(cls, kind, raw_value):
        if kind == 'int':
            return int(raw_value)

        if kind == 'json':
            return json.loads(raw_value)

        if kind == 'time':
            return time.strptime(raw_value, '%H:%M')

        if kind == 'date':
            return datetime.datetime.strptime(raw_value, '%Y-%m-%d')

        return raw_value

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
            return cls.process_value(kind, raw_value)

        try:
            parameter = Parameter.objects.get(
                name=name
            )
        except Parameter.DoesNotExist:
            parameter = Parameter.create_parameter(name)

        parameter.store_in_cache()

        return parameter.value

    @classmethod
    def create_all_parameters(cls):
        for parameter_definition in ParameterDefinitionList.definitions:
            cls.objects.get_or_create(
                name=parameter_definition.name,
                kind=parameter_definition.kind,
                defaults={
                    'raw_value': parameter_definition.default,
                }
            )

    @classmethod
    def create_parameter(cls, name):
        parameter_definition = ParameterDefinitionList.get_definition(name)

        return cls.objects.create(
            name=name,
            kind=parameter_definition.kind,
            raw_value=parameter_definition.default,
        )

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
