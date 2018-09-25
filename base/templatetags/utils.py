# -*- coding: utf-8 -*-
"""
Utils template tags
"""

# standard library


# django
from django import template


register = template.Library()


@register.filter
def group(array, group_length):
    """Yield successive n-sized chunks from l."""
    if array is None:
        array = []

    for i in range(0, len(array), group_length):
        yield array[i:i + group_length]
