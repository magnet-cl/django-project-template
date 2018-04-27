# -*- coding: utf-8 -*-
""" Forms for the parameters application. """
# standard library

# django
from django import forms

# models
from .models import Parameter

# views
from base.forms import BaseModelForm


class ParameterForm(BaseModelForm):
    """
    Form Parameter model.
    """

    class Meta:
        model = Parameter
        exclude = ()
