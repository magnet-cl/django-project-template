# -*- coding: utf-8 -*-
""" This file contains some generic purpouse views """

# standard library

# django
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from django.views.defaults import bad_request
from django.views.defaults import permission_denied
from django.views.defaults import page_not_found
from django.views.defaults import server_error

# utils
from base.view_utils import clean_query_string
from inflection import underscore


@login_required
def index(request):
    """ view that renders a default home"""
    return render(request, 'index.pug')


def bad_request_view(request, exception, template=None):
    return bad_request(request, exception, 'exceptions/400.pug')


def permission_denied_view(request, exception, template=None):
    return permission_denied(request, exception, 'exceptions/403.pug')


def page_not_found_view(request, exception, template=None):
    return page_not_found(request, exception, 'exceptions/404.pug')


def server_error_view(request, template=None):
    return server_error(request, 'exceptions/500.pug')


class PermissionRequiredMixin:
    permission_required = None

    def check_permission_required(self):
        if self.permission_required:
            if not self.request.user.has_perm(self.permission_required):
                raise PermissionDenied


class BaseDetailView(DetailView, PermissionRequiredMixin):

    def get_title(self):
        verbose_name = self.model._meta.verbose_name
        return '{}: {}'.format(verbose_name, self.object).title()

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['title'] = self.get_title()

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseDetailView, self).dispatch(*args, **kwargs)


class BaseCreateView(CreateView, PermissionRequiredMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data(**kwargs)

        verbose_name = self.model._meta.verbose_name
        context['opts'] = self.model._meta
        context['title'] = _('Create %s') % verbose_name
        context['cancel_url'] = self.get_cancel_url()

        return context

    def get_cancel_url(self):
        model_name = self.model.__name__.lower()
        return reverse('{}_list'.format(model_name))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseCreateView, self).dispatch(*args, **kwargs)


class BaseSubModelCreateView(CreateView, PermissionRequiredMixin):
    """
    Create view when the object is nested within a parent object
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseSubModelCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        model_underscore_name = underscore(self.parent_model.__name__)

        obj = get_object_or_404(
            self.parent_model,
            pk=self.kwargs['{}_id'.format(model_underscore_name)]
        )

        self.object = self.model(**{model_underscore_name: obj})

        return super(BaseSubModelCreateView, self).get_form_kwargs()

    def get_context_data(self, **kwargs):
        context = super(BaseSubModelCreateView, self).get_context_data(
            **kwargs
        )
        model_underscore_name = underscore(self.parent_model.__name__)

        obj = get_object_or_404(
            self.parent_model,
            pk=self.kwargs['{}_id'.format(model_underscore_name)]
        )

        context[model_underscore_name] = obj
        context['title'] = _('Create %s') % self.model._meta.verbose_name
        context['cancel_url'] = obj.get_absolute_url()

        return context


class BaseListView(ListView, PermissionRequiredMixin):
    paginate_by = 25
    page_kwarg = 'p'
    ignore_kwargs_on_filter = ('q', page_kwarg, 'o')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['clean_query_string'] = clean_query_string(self.request)
        context['q'] = self.request.GET.get('q')
        context['title'] = self.get_title()
        context['ordering'] = self.request.GET.getlist('o')
        return context

    def get_title(self):
        return self.model._meta.verbose_name_plural.title()

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        order = self.request.GET.getlist('o')
        if order:
            return order

        return self.ordering

    def get_queryset(self):
        """
        return the queryset to use on the list and filter by what comes on the
        query string
        """
        queryset = super(BaseListView, self).get_queryset()

        # obtain non ignored kwargs for the filter method
        items = self.request.GET.items()
        params = dict(
            (k, v) for k, v in items if k not in self.ignore_kwargs_on_filter
        )

        # filter
        for key, value in params.items():
            try:
                queryset = queryset.filter(**{key: value})
            except Exception:
                pass
        return queryset


class BaseTemplateView(TemplateView, PermissionRequiredMixin):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseTemplateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)

        context['title'] = self.title

        return context


class BaseUpdateView(UpdateView, PermissionRequiredMixin):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['cancel_url'] = self.get_cancel_url()
        context['title'] = _('Update %s') % str(self.object)

        return context

    def get_cancel_url(self):
        return self.object.get_absolute_url()


class BaseDeleteView(DeleteView, PermissionRequiredMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseDeleteView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['title'] = _('Delete %s') % str(self.object)

        return context

    def get_success_url(self):
        model_name = self.model.__name__.lower()
        return reverse('{}_list'.format(model_name))


class BaseRedirectView(RedirectView, PermissionRequiredMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseRedirectView, self).dispatch(*args, **kwargs)


class BaseUpdateRedirectView(
        PermissionRequiredMixin, SingleObjectMixin, RedirectView):

    permanent = False

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseUpdateRedirectView, self).get(
            request, *args, **kwargs
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.do_action()
        return super(BaseUpdateRedirectView, self).post(
            request, *args, **kwargs
        )

    def do_action():
        """
        Implement this method with the action you want to do before redirect
        """
        pass

    def get_redirect_url(self, *args, **kwargs):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url

        return self.object.get_absolute_url()


@method_decorator(staff_member_required, name='dispatch')
class StatusView(BaseTemplateView):
    template_name = 'status.pug'
    title = _('status').title()

    def get_context_data(self, **kwargs):
        context = super(StatusView, self).get_context_data(**kwargs)

        context['settings'] = settings

        return context
