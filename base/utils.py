""" Small methods for generic use """

# standard library
from itertools import cycle
import itertools
import os
import random
import re
import string
import unicodedata
import datetime
import pytz

# django
from django.apps import apps
from django.utils import timezone
from django.db import models


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
    if type(verifier) == str:
        verifier = verifier.upper()

    code = rut[0:-1][::-1]

    code = re.sub("(.{3})", "\\1.", code, 0, re.DOTALL)

    code = code[::-1]

    return '%s-%s' % (code, verifier)


def validate_rut(rut):
    rut = rut.lower()
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    rut = rut.replace(" ", "")
    aux = rut[:-1]
    dv = rut[-1:]

    rev = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(rev, factors))
    res = (-s) % 11

    if str(res) == dv:
        return True
    elif dv == "k" and res == 10:
        return True
    else:
        return False


def strip_accents(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def tz_datetime(*args, **kwargs):
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


def can_loginas(request, target_user):
    """ This will only allow admins to log in as other users """
    return request.user.is_superuser and not target_user.is_superuser


def date_to_datetime(date):
    tz = timezone.get_default_timezone()

    try:
        r_datetime = timezone.make_aware(
            datetime.datetime.combine(
                date,
                datetime.datetime.min.time()),
            tz
        )
    except pytz.NonExistentTimeError:
        r_datetime = timezone.make_aware(
            datetime.datetime.combine(
                date,
                datetime.datetime.min.time()
            ) + datetime.timedelta(hours=1),
            tz
        )

    except pytz.AmbiguousTimeError:
        r_datetime = timezone.make_aware(
            datetime.datetime.combine(
                date,
                datetime.datetime.min.time()
            ) - datetime.timedelta(hours=1),
            tz
        )

    return r_datetime


def get_slug_fields(model):
    slug_fields = []
    for field in model._meta.fields:
        if isinstance(field, models.SlugField):
            slug_fields.append(field)
    return slug_fields
