# -*- coding: utf-8 -*-
""" This file contains some generic purpouse views """

# standard library

# django
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured
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


class LoginPermissionRequiredMixin(AccessMixin):
    """
    Verify that the current user is authenticated (if required)
    and has the required permission (if authenticated)
    """
    permission_required = None

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. '
                'Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(
                    self.__class__.__name__
                )
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def dispatch(self, request, *args, **kwargs):
        if self.login_required:
            if not request.user.is_authenticated:
                return self.handle_no_permission()

            if not self.has_permission():
                return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)


class BaseDetailView(LoginPermissionRequiredMixin, DetailView):
    login_required = True
    permission_required = ()

    def get_title(self):
        verbose_name = self.model._meta.verbose_name
        return '{}: {}'.format(verbose_name, self.object).title()

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['title'] = self.get_title()

        return context


class BaseCreateView(LoginPermissionRequiredMixin, CreateView):
    login_required = True
    permission_required = ()

    next_url = None

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data(**kwargs)

        self.next_url = self.request.GET.get('next')

        context['next'] = self.next_url

        verbose_name = self.model._meta.verbose_name
        context['opts'] = self.model._meta
        context['title'] = _('Create %s') % verbose_name
        context['cancel_url'] = self.get_cancel_url()

        return context

    def get_cancel_url(self):
        if self.next_url:
            return self.next_url

        model_name = self.model.__name__.lower()
        return reverse('{}_list'.format(model_name))

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url

        return super().get_success_url()


class BaseSubModelCreateView(LoginPermissionRequiredMixin, CreateView):
    """
    Create view when the object is nested within a parent object
    """
    login_required = True
    permission_required = ()

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


class BaseListView(LoginPermissionRequiredMixin, ListView):
    login_required = True
    permission_required = ()
    paginate_by = 25
    page_kwarg = 'p'
    ignore_kwargs_on_filter = ('q', page_kwarg, 'o')

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


class BaseTemplateView(LoginPermissionRequiredMixin, TemplateView):
    login_required = True
    permission_required = ()

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)

        context['title'] = self.title

        return context


class BaseUpdateView(LoginPermissionRequiredMixin, UpdateView):
    login_required = True
    permission_required = ()
    next_url = None

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data(**kwargs)

        self.next_url = self.request.GET.get('next')

        context['next'] = self.next_url

        context['opts'] = self.model._meta
        context['cancel_url'] = self.get_cancel_url()
        context['title'] = _('Update %s') % str(self.object)

        return context

    def get_cancel_url(self):
        if self.next_url:
            return self.next_url

        return self.object.get_absolute_url()

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url

        return super().get_success_url()


class BaseDeleteView(LoginPermissionRequiredMixin, DeleteView):
    login_required = True
    permission_required = ()
    next_url = None

    def get_context_data(self, **kwargs):
        context = super(BaseDeleteView, self).get_context_data(**kwargs)

        self.next_url = self.request.GET.get('next')

        context['next'] = self.next_url

        context['opts'] = self.model._meta
        context['title'] = _('Delete %s') % str(self.object)

        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url

        model_name = self.model.__name__.lower()
        return reverse('{}_list'.format(model_name))


class BaseRedirectView(LoginPermissionRequiredMixin, RedirectView):
    login_required = True
    permission_required = ()


class BaseUpdateRedirectView(LoginPermissionRequiredMixin, SingleObjectMixin,
                             RedirectView):
    login_required = True
    permission_required = ()

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


class FormsetViewMixin:
    formset_class = None
    initial_formset = {}
    prefix_formset = None

    def get_formset_class(self):
        return self.formset_class

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = self.get_formset()
        form = self.get_form()
        return self.render_to_response(
            self.get_context_data(formset=formset, form=form)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form_valid = super().form_valid(form)
        formset.instance = self.object
        formset.save()
        return form_valid

    def get_initial_formset(self):
        """Return the initial data to use for formset on this view."""
        return self.initial_formset.copy()

    def get_prefix_formset(self):
        """Return the prefix to use for formset."""
        return self.prefix_formset

    def get_formset_kwargs(self):
        kwargs = {
            'initial': self.get_initial_formset(),
            'prefix': self.get_prefix_formset(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_formset(self, formset_class=None):
        """Return an instance of the form to be used in this view."""
        if formset_class is None:
            formset_class = self.get_formset_class()
        return formset_class(**self.get_formset_kwargs())

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class FormsetCreateView(FormsetViewMixin, BaseCreateView):

    def get_object(self, queryset=None):
        return None


class FormsetUpdateView(FormsetViewMixin, BaseUpdateView):

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating formset."""
        kwargs = super().get_formset_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs
