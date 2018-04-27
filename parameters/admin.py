# -*- coding: utf-8 -*-
""" Administration classes for the parameters application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Parameter


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    pass
