# -*- coding: utf-8 -*-
""" Models for the users application.

All apps should use the users.User model for all users
"""
# django
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.template import loader
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop

# managers
from users.managers import UserManager

# models
from base.models import BaseModel
from parameters.models import Parameter

# messaging
from messaging import email_manager

# mark for translation the app name
ugettext_noop("Users")


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    User model with admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """

    # required fields
    email = models.EmailField(
        _('email address'),
        unique=True,
        db_index=True,
    )
    # optional fields
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=30,
        blank=True,
    )
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'),
    )
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'),
    )
    # auto fields
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now,
        help_text=_("The date this user was created in the database"),
    )
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # public methods
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    # overwritten methods
    def save(self, *args, **kwargs):
        """ store all emails in lowercase """
        self.email = self.email.lower()

        super(User, self).save(*args, **kwargs)

    def send_example_email(self):
        email_manager.send_example_email(self.email)

    def send_recover_password_email(self, request=None):
        """
        Sends an email with the required token so a user can recover
        his/her password

        """
        template = "password_reset"

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        template_vars = {
            'email': self.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'user': self,
            'token': default_token_generator.make_token(self),
            'protocol': Parameter.value_for('DEFAULT_URL_PROTOCOL'),
        }

        subject_template_name = 'registration/password_reset_subject.txt'
        title = loader.render_to_string(subject_template_name, template_vars)

        email_manager.send_emails(
            emails=(self.email,),
            template_name=template,
            subject=title,
            context=template_vars
        )

    def force_logout(self):
        """
        Deletes all the sessions of the User
        """
        # delete all the sessions that match the user
        for s in Session.objects.all():
            if int(s.get_decoded().get('_auth_user_id')) == self.id:
                s.delete()
