""" this document defines the users app urls """
from django.conf.urls import url

from users import views as users_views

urlpatterns = [
    url(
        r'^login/$',
        users_views.login,
        name='login'
    ),
    url(
        r'^password-change/$',
        users_views.password_change,
        name='password_change'
    ),
    url(
        r'^logout/$',
        users_views.logout,
        name='logout'
    ),
    url(
        r'^register/$',
        users_views.user_new,
        name='register',
    ),
    url(
        r'^password-email-sent/$',
        users_views.password_reset_email_sent,
        name='password_email_sent'
    ),
    url(
        r'^password-reset/$',
        users_views.password_reset,
        name='password_reset'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        users_views.password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(
        r'^verify/(?P<uidb36>[0-9A-Za-z]{1,13})-'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        users_views.user_new_confirm,
        name='user_new_confirm'
    ),
    url(
        r'^reset/done/$',
        users_views.password_reset_complete,
        name='password_reset_complete'
    ),
    url(
        r'^edit/$',
        users_views.user_edit,
        name='user_edit'
    ),
    url(
        r'^profile/$',
        users_views.user_profile,
        name='user_profile'
    ),
]
