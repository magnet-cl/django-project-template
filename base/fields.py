# -*- coding: utf-8 -*-
""" 
Custom Fields
"""

# standard library
import re

# django
from django.db.models import CharField
from django.core.exceptions import ValidationError

# utils
from base import utils

# translations
from django.utils.translation import ugettext_lazy as _


class ChileanRUTField(CharField):
    """
    A model field that stores a Chilean RUT in the format "XX.XXX.XXX-Y".
    Letters are stored in uppercase.
    """
    description = _("Chilean RUT (up to %(max_length)s)")
    default_error_messages = {
        'invalid_format': _(
            "'%(value)s' value has an invalid format. "
            "It must be in XX.XXX.XXX-Y format or "
            "XXXXXXXXY format."
        ),
        'invalid_rut': _(
            "'%(value)s' value has the correct format "
            " but it is an invalid rut."
        ),
        'invalid_type': _(
            "'%(value)s' must be str or None."
        ),
    }

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value
        elif not isinstance(value, str):
            raise ValidationError(
                self.error_messages['invalid_type'],
                code='invalid',
                params={'value': value},
            )
        value = self._format_rut(value)
        if value == '' or value is None:
            return value
        if not utils.validate_rut(value):
            raise ValidationError(
                self.error_messages['invalid_rut'],
                code='invalid',
                params={'value': value},
            )
        return value

    def _format_rut(self, value):
        value = value.strip()
        full_format = re.compile(r'[1-9]\d{0,2}(\.\d{3})*-[\dkK]')
        incomplete_format = re.compile(r'[1-9](\d)*[\dkK]')
        if value == '':
            return value
        elif re.fullmatch(full_format, value):
            value = value[:-1] + value[-1].upper()
        elif re.fullmatch(incomplete_format, value):
            value = utils.format_rut(value)
            value = value[:-1] + value[-1].upper()
        else:
            raise ValidationError(
                self.error_messages['invalid_format'],
                code='invalid',
                params={'value': value},
            )
        return value
