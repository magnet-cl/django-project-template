# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^communes/search/$',
        views.search_communes,
        name='search_communes'
    ),
]
