# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_users(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model('users', 'User')

    User.objects.create(
        date_joined='2012-10-09T21:42:23Z',
        email='alex.smith@example.com',
        first_name='Alex',
        is_active=True,
        is_staff=True,
        is_superuser=True,
        last_name='Smith',
        password=make_password('codigofuente'),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]
