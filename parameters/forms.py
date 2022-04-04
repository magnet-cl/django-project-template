# -*- coding: utf-8 -*-
""" Forms for the parameters application. """
# standard library

# django
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.widgets import AdminTimeWidget

# models
from .models import Parameter

# views
from base.forms import BaseModelForm

# enums
from parameters.enums import ParameterKinds


class ParameterForm(BaseModelForm):
    """
    Form Parameter model.
    """

    class Meta:
        model = Parameter
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.kind == ParameterKinds.BOOL:
            self.fields['raw_value'].widget = forms.Select(
                choices=(
                    ('True', 'True'),
                    ('False', 'False'),
                )
            )
        elif self.instance.kind == ParameterKinds.INT:
            self.fields['raw_value'].widget = forms.NumberInput()
        elif self.instance.kind == ParameterKinds.DATE:
            self.fields['raw_value'].widget = AdminDateWidget()
        elif self.instance.kind == ParameterKinds.TIME:
            self.fields['raw_value'].widget = AdminTimeWidget()
