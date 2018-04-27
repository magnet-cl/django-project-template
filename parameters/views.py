# -*- coding: utf-8 -*-
""" Views for the parameters application. """
# standard library

# django

# models
from .models import Parameter

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import ParameterForm


class ParameterListView(BaseListView):
    """
    View for displaying a list of parameters.
    """
    model = Parameter
    template_name = 'parameters/parameter_list.pug'
    permission_required = 'parameters.view_parameter'


class ParameterCreateView(BaseCreateView):
    """
    A view for creating a single parameter
    """
    model = Parameter
    form_class = ParameterForm
    template_name = 'parameters/parameter_create.pug'
    permission_required = 'parameters.add_parameter'


class ParameterDetailView(BaseDetailView):
    """
    A view for displaying a single parameter
    """
    model = Parameter
    template_name = 'parameters/parameter_detail.pug'
    permission_required = 'parameters.view_parameter'


class ParameterUpdateView(BaseUpdateView):
    """
    A view for editing a single parameter
    """
    model = Parameter
    form_class = ParameterForm
    template_name = 'parameters/parameter_update.pug'
    permission_required = 'parameters.change_parameter'


class ParameterDeleteView(BaseDeleteView):
    """
    A view for deleting a single parameter
    """
    model = Parameter
    permission_required = 'parameters.delete_parameter'
    template_name = 'parameters/parameter_delete.pug'
