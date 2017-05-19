# -*- coding: utf-8 -*-
""" The users app views"""

# forms
from users.forms import AuthenticationForm
from users.forms import CaptchaAuthenticationForm
from users.forms import CaptchaUserCreationForm
from users.forms import UserForm

# models
from users.models import User

# django
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login as django_login_view
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.http import base36_to_int
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters


def login(request):
    """ view that renders the login """

    if request.user.is_authenticated():
        return redirect('home')

    def captched_form(req=None, data=None):
        return CaptchaAuthenticationForm(
            req, data, initial={'captcha': request.META['REMOTE_ADDR']})

    template_name = "accounts/login.pug"

    login_try_count = request.session.get('login_try_count', 0)

    # If the form has been submitted...
    if request.method == "POST":
        request.session['login_try_count'] = login_try_count + 1

    if login_try_count >= 2:
        return django_login_view(request, authentication_form=captched_form,
                                 template_name=template_name)

    return django_login_view(request, authentication_form=AuthenticationForm,
                             template_name=template_name)


def logout(request):
    """ view that handles the logout """
    django_logout(request)
    return redirect('home')


@login_required
def password_change(request):
    """ view that renders the login """
    # If the form has been submitted...
    template_name = "accounts/password_change.pug"

    return auth_views.password_change(request, post_change_redirect="/",
                                      template_name=template_name)


def password_reset(request):
    """ view that handles the recover password process """

    template_name = "accounts/password_reset_form.pug"
    email_template_name = "emails/password_reset.html"

    success_url = "/accounts/password-email-sent"

    res = auth_views.password_reset(
        request,
        post_reset_redirect=success_url,
        template_name=template_name,
        email_template_name=email_template_name)
    return res


def password_reset_email_sent(request):
    messages.add_message(request, messages.INFO,
                         _("An email has been sent to you. Please check it "
                           "to reset your password."))
    return redirect('home')


def password_reset_confirm(request, uidb64, token):
    """ view that handles the recover password process """
    template_name = "accounts/password_reset_confirm.html"
    success_url = "/accounts/reset/done/"

    return auth_views.password_reset_confirm(request, uidb64, token,
                                             template_name=template_name,
                                             post_reset_redirect=success_url)


def password_reset_complete(request):
    """ view that handles the recover password process """

    template_name = "accounts/password_reset_complete.html"
    return auth_views.password_reset_complete(request,
                                              template_name=template_name)


def user_new(request):
    if request.method == 'POST':
        form = CaptchaUserCreationForm(
            request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.save(verify_email_address=True, request=request)
            messages.add_message(request, messages.INFO,
                                 _("An email has been sent to you. Please "
                                   "check it to verify your email."))
            return redirect('home')
    else:
        form = CaptchaUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/user_new.html', context)


@login_required
def user_edit(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Your data has been successfully saved."))
            return redirect('home')
    else:
        form = UserForm(instance=request.user)

    context = {
        'cancel_url': reverse('user_profile'),
        'form': form,
    }

    return render(request, 'accounts/edit.pug', context)


@login_required
def user_profile(request):
    context = {
    }

    return render(request, 'accounts/detail.pug', context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def user_new_confirm(request, uidb36=None, token=None,
                     token_generator=default_token_generator,
                     current_app=None, extra_context=None):
    """
    View that checks the hash in a email confirmation link and activates
    the user.
    """

    assert uidb36 is not None and token is not None  # checked by URLconf
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.update(is_active=True)
        messages.add_message(request, messages.INFO,
                             _("Your email address has been verified."))
    else:
        messages.add_message(request, messages.ERROR,
                             _("Invalid verification link"))

    return redirect('login')
