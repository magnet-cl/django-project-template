# -*- coding: utf-8 -*-

DEBUG = True

LOCAL_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'circle_test',
        'USER': 'circleci',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    },
     'logs': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'circle_test_logs',
        'USER': 'circleci',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LOCALLY_INSTALLED_APPS = [
]

ENABLE_EMAILS = False

LOCALLY_ALLOWED_HOSTS = [
]

ADMINS = []

SECRET_KEY = 'CHANGE ME'
