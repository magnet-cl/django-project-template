""" This document defines the UserManager class"""

# django
from django.db.models import Q
from django.contrib.auth.models import BaseUserManager

# base
from base.managers import QuerySet


class UserQuerySet(QuerySet):
    def search(self, query):

        queryset = self

        for term in query.split(' '):
            queryset = queryset.filter(
                Q(first_name__unaccent__icontains=term) |
                Q(last_name__unaccent__icontains=term) |
                Q(email__icontains=term)
            )

        return queryset


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name,
                     password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, first_name=None, last_name=None,
                    password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, first_name=None,
                         last_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, first_name, last_name,
                                 password, **extra_fields)

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def to_json(self):
        return self.get_queryset().to_json()

    def find_duplicates(self, *fields):
        return self.get_queryset().find_duplicates(*fields)

    def get_or_none(self, **fields):
        return self.get_queryset().get_or_none(**fields)
