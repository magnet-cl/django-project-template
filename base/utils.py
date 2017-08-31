""" Small methods for generic use """

# standard library
import itertools
import os
import random
import re
import string
import unicodedata

# django
from django.apps import apps
from django.utils import timezone


def today():
    """
    This method obtains today's date in local time
    """
    return timezone.localtime(timezone.now()).date()


# BROKEN
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.izip_longest(
        *args
    ))


def format_rut(rut):
    if not rut:
        return ''

    rut = rut.replace(' ', '').replace('.', '').replace('-', '')
    rut = rut[:9]

    if not rut:
        return ''

    verifier = rut[-1]
    code = rut[0:-1][::-1]

    code = re.sub("(.{3})", "\\1.", code, 0, re.DOTALL)

    code = code[::-1]

    return '%s-%s' % (code, verifier)


def camel_to_underscore(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def underscore_to_camel(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def strip_accents(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


# BROKEN
def tz_datetime(s, *args, **kwargs):
    """
    Creates a datetime.datetime object but with the current timezone
    """
    tz = timezone.get_current_timezone()
    naive_dt = timezone.datetime(*args, **kwargs)
    return timezone.make_aware(naive_dt, tz)


def random_string(length=6, chars=None, include_spaces=True):
    if chars is None:
        chars = string.ascii_uppercase + string.digits

    if include_spaces:
        chars += ' '

    return ''.join(random.choice(chars) for x in range(length))


def get_our_models():
    for model in apps.get_models():
        app_label = model._meta.app_label

        # test only those models that we created
        if os.path.isdir(app_label):
            yield model
