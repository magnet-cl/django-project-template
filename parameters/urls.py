from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.ParameterListView.as_view(),
        name='parameter_list'
    ),
    path(
        'create/',
        views.ParameterCreateView.as_view(),
        name='parameter_create'
    ),
    path(
        '<int:pk>/',
        views.ParameterDetailView.as_view(),
        name='parameter_detail'
    ),
    path(
        '<int:pk>/update/',
        views.ParameterUpdateView.as_view(),
        name='parameter_update'
    ),
    path(
        '<int:pk>/delete/',
        views.ParameterDeleteView.as_view(),
        name='parameter_delete',
    ),
]
