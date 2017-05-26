# -*- coding: utf-8 -*-
""" The users app views"""

# django
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.http import base36_to_int
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import CreateView

# forms
from users.forms import AuthenticationForm
from users.forms import CaptchaAuthenticationForm
from users.forms import CaptchaUserCreationForm
from users.forms import UserForm

# models
from users.models import User

# views


class LoginView(auth_views.LoginView):
    """ view that renders the login """
    template_name = "registration/login.pug"
    form_class = AuthenticationForm

    def get_form_class(self):
        """
        Returns the form class, if the user has tried too many times to login
        without success, then it passes on the captcha login
        """
        login_try_count = self.request.session.get('login_try_count', 0)

        # If the form has been submitted...
        if self.request.method == "POST":
            self.request.session['login_try_count'] = login_try_count + 1

        if login_try_count >= 20:
            return CaptchaAuthenticationForm

        return super(LoginView, self).get_form_class()


class LogoutView(auth_views.LogoutView):
    next_page = 'home'


class PasswordChangeView(auth_views.PasswordChangeView):
    """ view that renders the password change form """
    template_name = "registration/password_change_form.pug"


class PasswordResetView(auth_views.PasswordResetView):
    """ view that handles the recover password process """
    template_name = "registration/password_reset_form.pug"
    email_template_name = "emails/password_reset.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """ view that handles the recover password process """
    template_name = "registration/password_reset_confirm.pug"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """ View that shows a success message to the user"""
    template_name = "registration/password_reset_complete.pug"


class UserCreateView(CreateView):
    template_name = 'users/create.pug'
    form_class = CaptchaUserCreationForm

    def form_valid(self, form):
        form.save(verify_email_address=True, request=self.request)
        messages.add_message(
            self.request,
            messages.INFO,
            _("An email has been sent to you. Please "
              "check it to verify your email.")
        )

        return redirect('home')


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
