from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.ParameterListView.as_view(),
        name='parameter_list'
    ),
    url(
        r'^create/$',
        views.ParameterCreateView.as_view(),
        name='parameter_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.ParameterDetailView.as_view(),
        name='parameter_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.ParameterUpdateView.as_view(),
        name='parameter_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.ParameterDeleteView.as_view(),
        name='parameter_delete',
    ),
]
