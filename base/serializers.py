# -*- coding: utf-8 -*-
""" Models for the base application.

All apps should use the BaseModel as parent for all models
"""

# standard library
import decimal

# django
from django.db import models
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder


class ModelEncoder(DjangoJSONEncoder):
    def default(self, obj):
        from base.models import BaseModel

        if isinstance(obj, models.fields.files.FieldFile):
            if obj:
                return obj.url
            else:
                return None

        elif isinstance(obj, BaseModel):
            return obj.to_dict()

        elif isinstance(obj, decimal.Decimal):
            return str(obj)

        elif isinstance(obj, Promise):
            return force_text(obj)

        return super(ModelEncoder, self).default(obj)
