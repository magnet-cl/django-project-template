"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# standard library

# django
from django.conf import settings
from django.contrib import admin
from django.urls import NoReverseMatch
from django.urls import reverse
from django.test import TestCase
from django.urls.converters import SlugConverter

# django-cron
from django_cron import get_class

# urls
from project.urls import urlpatterns

# utils
from inflection import underscore
from base.utils import get_our_models
from base.utils import random_string
from base.mockups import Mockup
from base.utils import get_slug_fields

# base
from base.middleware import RequestMiddleware


class BaseTestCase(TestCase, Mockup):

    def setUp(self):
        super(BaseTestCase, self).setUp()

        self.password = random_string()
        self.user = self.create_user(self.password)

        self.login()

    def tearDown(self, *args, **kwargs):
        super().tearDown(*args, **kwargs)
        thread_local = RequestMiddleware.thread_local
        thread_local.user = None

    def login(self, user=None, password=None):
        if user is None:
            user = self.user
            password = self.password

        return self.client.login(email=user.email, password=password)


def reverse_pattern(pattern, namespace, args=None, kwargs=None):
    try:
        if namespace:
            return reverse('{}:{}'.format(
                namespace, pattern.name)
            )
        else:
            return reverse(pattern.name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return None


class UrlsTest(BaseTestCase):

    def setUp(self):
        super(UrlsTest, self).setUp()

        # we are going to send parameters, so one thing we'll do is to send
        # tie id 1
        self.user.delete()
        self.user.id = 1

        # give the user all the permissions, so we test every page
        self.user.is_superuser = True

        self.user.save()
        self.login()

        # store default values for urls. E.g. user_id
        self.default_params = {}

        # store default objects to get foreign key parameters
        self.default_objects = {}

        for model in get_our_models():
            model_name = underscore(model.__name__)
            method_name = 'create_{}'.format(model_name)

            # store the created object
            obj = getattr(self, method_name)(**self.get_obj_kwargs(model))
            self.default_objects[model_name] = obj

            self.assertIsNotNone(obj, '{} returns None'.format(method_name))

            # store the object id with the expected name a url should use
            # when using object ids:
            param_name = '{}_id'.format(model_name)
            self.default_params[param_name] = obj.id
            for slug_field in get_slug_fields(model):
                value = getattr(obj, slug_field.name)
                param_name = '{}_{}_slug'.format(model_name, slug_field.name)
                self.default_params[param_name] = value

    def get_obj_kwargs(self, model):
        """
        When testing all urls, there are business logic that require certain
        values on the objects we are creating. This method returns a kwrags
        diciontary to be passed to the create_X method that creaates an
        instance of model.

        For example, imagine that APP has the url /message/1/
        It is reasonable that the view will return 404 if the logged in user
        has no nothing to do with.
        This method will be called when creating the test objects to be used
        on the UrlsTest, in our example a solution would be to return a
        dictionary where the user is the logged in user
        return {"user": self.user}
        """
        return {}

    def get_url_using_param_names(self, url_pattern, namespace):
        """
        Using the dictionary of parameters defined on self.default_params and
        the list of objects defined on self.default_objects, construct urls
        with valid parameters.

        This method assumes that nested urls name their parents ids as
        {model}_id

        Thus something like the comments of a user should be in the format of

        '/users/{user_id}/comments/'
        """
        param_converter_name = url_pattern.pattern.converters.items()

        params = {}
        if not param_converter_name:
            return

        callback = url_pattern.callback

        obj = None

        for param_name, converter in param_converter_name:
            if param_name == 'pk' and hasattr(callback, 'view_class'):
                model_name = underscore(
                    url_pattern.callback.view_class.model.__name__
                )
                params['pk'] = self.default_params['{}_id'.format(model_name)]
                obj = self.default_objects[model_name]
            elif isinstance(converter, SlugConverter) and hasattr(callback, 'view_class'): # noqa
                model_name = underscore(
                    url_pattern.callback.view_class.model.__name__
                )
                params[param_name] = self.default_params[
                    '{}_{}_slug'.format(model_name, param_name)
                ]
                obj = self.default_objects[model_name]
            else:
                try:
                    params[param_name] = self.default_params[param_name]
                except KeyError:
                    return None

        if obj:
            # if the object has an attribute named as the parameter
            # assume it should be used on the url, since many views
            # filter nested objects
            for param in params:
                if hasattr(obj, param) and getattr(obj, param):
                    params[param] = getattr(obj, param)

        return reverse_pattern(url_pattern, namespace, kwargs=params)

    def reverse_pattern(self, url_pattern, namespace):
        url = self.get_url_using_param_names(url_pattern, namespace)
        if url:
            return url

        param_names = url_pattern.pattern.regex.groupindex.keys()
        url_params = {}

        for param in param_names:
            try:
                url_params[param] = self.default_params[param]
            except KeyError:
                url_params[param] = 1

        return reverse_pattern(url_pattern, namespace, kwargs=url_params)

    def test_responses(self):

        ignored_namespaces = [
            'admin',
        ]

        def test_url_patterns(patterns, namespace=''):

            if namespace in ignored_namespaces:
                return

            for pattern in patterns:
                self.login()

                if hasattr(pattern, 'name'):
                    url = self.reverse_pattern(pattern, namespace)

                    if not url:
                        continue

                    try:
                        response = self.client.get(url)
                    except Exception:
                        print("Url {} failed: ".format(url))
                        raise

                    msg = 'url "{}" ({})returned {}'.format(
                        url, pattern.name, response.status_code
                    )
                    self.assertIn(
                        response.status_code,
                        (200, 302, 403, 405), msg
                    )
                else:
                    test_url_patterns(pattern.url_patterns, pattern.namespace)

        test_url_patterns(urlpatterns)

        for model, model_admin in admin.site._registry.items():
            patterns = model_admin.get_urls()
            test_url_patterns(patterns, namespace='admin')


class CheckErrorPages(TestCase):
    def test_404(self):
        response = self.client.get('/this-url-does-not-exist')
        self.assertTemplateUsed(response, 'exceptions/404.pug')


class CronTests(BaseTestCase):
    def test_cron_classes_to_run(self):
        """
        Asserts that a cron class name can be imported using the canonical name
        given in project settings
        """

        cron_class_names = getattr(settings, 'CRON_CLASSES', [])
        for cron_class_name in cron_class_names:
            assert get_class(cron_class_name)
