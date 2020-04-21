# -*- coding: utf-8 -*-

from django.urls import path

from . import views

urlpatterns = [
    path(
        'communes/search/',
        views.search_communes,
        name='search_communes'
    ),
]
