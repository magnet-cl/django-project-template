""" this document defines the users app urls """
from django.urls import path
from django.contrib.auth import views as auth_views

from users import views as users_views

urlpatterns = [
    path(
        '',
        users_views.UserListView.as_view(),
        name='user_list',
    ),
    path(
        'login/',
        users_views.LoginView.as_view(),
        name='login'
    ),
    path(
        'password-change/',
        users_views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password-change/done/',
        users_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'register/',
        users_views.UserCreateView.as_view(),
        name='register',
    ),
    path(
        'password-reset/',
        users_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'reset/<uidb64>/<token>/',
        users_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'verify/<uidb36>/<token>/',
        users_views.user_new_confirm,
        name='user_new_confirm'
    ),
    path(
        'reset/done/',
        users_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
        'password-reset/done/',
        users_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'edit/',
        users_views.user_edit,
        name='user_edit'
    ),
    path(
        'profile/',
        users_views.user_profile,
        name='user_profile'
    ),
]
