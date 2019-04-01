"""
This file has the Mockup class, that creates randomn instances of the
project models
"""

# standard library
from shutil import copyfile
import os
import random
import string
import uuid

# django
from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.utils import timezone

# models
from parameters.models import Parameter
from regions.models import Commune
from regions.models import Region
from users.models import User

# utils
from inflection import underscore
from base.utils import random_string


class Mockup(object):
    def create_commune(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_foreign_key(kwargs, 'region')
        return Commune.objects.create(**kwargs)

    def create_parameter(self, **kwargs):
        return Parameter.objects.create(**kwargs)

    def create_region(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        return Region.objects.create(**kwargs)

    def create_user(self, password=None, **kwargs):
        if kwargs.get('first_name') is None:
            kwargs['first_name'] = random_string(length=6)

        if kwargs.get('last_name') is None:
            kwargs['last_name'] = random_string(length=6)

        if kwargs.get('email') is None:
            kwargs['email'] = "%s@gmail.com" % random_string(length=6)

        if kwargs.get('is_active') is None:
            kwargs['is_active'] = True

        user = User.objects.create(**kwargs)

        if password is not None:
            user.set_password(password)
            user.save()

        return user

    def random_email(self):
        return "{}@{}.{}".format(
            random_string(length=6),
            random_string(length=6),
            random_string(length=2)
        )

    def random_hex_int(self, *args, **kwargs):
        val = self.random_int(*args, **kwargs)
        return hex(val)

    def random_int(self, minimum=-100000, maximum=100000):
        return random.randint(minimum, maximum)

    def random_float(self, minimum=-100000, maximum=100000):
        return random.uniform(minimum, maximum)

    def random_uuid(self, *args, **kwargs):
        chars = string.digits
        return uuid.UUID(''.join(random.choice(chars) for x in range(32)))

    def set_required_boolean(self, data, field, default=None, **kwargs):
        if field not in data:

            if default is None:
                data[field] = not not random.randint(0, 1)
            else:
                data[field] = default

    def set_required_choice(self, data, field, choices, **kwargs):
        if field not in data:
            data[field] = random.choice(choices)[0]

    def set_required_date(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().date()

    def set_required_datetime(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now()

    def set_required_email(self, data, field):
        if field not in data:
            data[field] = self.random_email()

    def set_required_file(self, data, field):
        if field in data:
            # do nothing if the field is in the data
            return

        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        test_root = os.path.realpath(os.path.dirname(__file__))

        file_path = data.pop('{}_file_path'.format(field), None)

        if file_path is None:
            file_path = 'gondola.jpg'

        if not os.path.isfile(file_path):
            file_path = '{}/test_assets/{}'.format(test_root, file_path)

        final_path = '{}{}'.format(
            settings.MEDIA_ROOT,
            os.path.basename(file_path)
        )

        copyfile(file_path, final_path)

        data[field] = File(open(final_path, 'rb'))

    def set_required_float(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_float(**kwargs)

    def set_required_foreign_key(self, data, field, model=None, **kwargs):
        if model is None:
            model = field

        if field not in data and '{}_id'.format(field) not in data:
            data[field] = getattr(self, 'create_{}'.format(model))(**kwargs)

    def set_required_int(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_int(**kwargs)

    def set_required_ip_address(self, data, field, **kwargs):
        if field not in data:
            ip = '{}.{}.{}.{}'.format(
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
            )
            data[field] = ip

    def set_required_rut(self, data, field, length=6):
        if field not in data:
            rut = '{}.{}.{}-{}'.format(
                self.random_int(minimum=1, maximum=99),
                self.random_int(minimum=100, maximum=990),
                self.random_int(minimum=100, maximum=990),
                random_string(length=1, chars='k' + string.digits),
            )
            data[field] = rut

    def set_required_string(self, data, field, length=6, include_spaces=True):
        if field not in data:
            data[field] = random_string(
                length=length,
                include_spaces=include_spaces,
            )

    def set_required_url(self, data, field, length=6):
        if field not in data:
            data[field] = 'http://{}.com'.format(
                random_string(length=length))


def add_get_or_create(cls, model):
    model_name = underscore(model.__name__)

    def get_or_create(self, **kwargs):
        try:
            return model.objects.get(**kwargs), False
        except model.DoesNotExist:
            pass

        method_name = 'create_{}'.format(model_name)
        return getattr(cls, method_name)(self, **kwargs), True

    get_or_create.__doc__ = "Get or create for {}".format(model_name)
    get_or_create.__name__ = "get_or_create_{}".format(model_name)
    setattr(cls, get_or_create.__name__, get_or_create)


def get_our_models():
    for model in apps.get_models():
        app_label = model._meta.app_label

        # test only those models that we created
        if os.path.isdir(app_label):
            yield model


for model in get_our_models():
    add_get_or_create(Mockup, model)
