# -*- coding: utf-8 -*-
""" Administration classes for the parameters application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Parameter
from parameters.enums import ParameterDefinitionList


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'raw_value', 'cache_seconds')

    def get_changelist_instance(self, request):
        """
        Return the ChangeList class for use on the changelist page.
        """
        expected_parameters_count = len(ParameterDefinitionList.definitions)

        if Parameter.objects.count() != expected_parameters_count:
            Parameter.create_all_parameters()

        change_list = super().get_changelist_instance(request)
        return change_list

    def has_add_permission(self, request, obj=None):
        return False
