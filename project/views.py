# -*- coding: utf-8 -*-
""" This file contains some generic views """

# django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """ view that renders a default home"""
    return render(request, 'index.pug')
