# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop

# base
from base.models import BaseModel

# mark for translation the app name
ugettext_noop('Regions')


class Region(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True,
        help_text=_('The name of the region'),
    )
    short_name = models.CharField(
        _('short name'),
        max_length=100,
        null=True,
        blank=True,
        unique=True,
        help_text=_('A short name of the region'),
    )
    order = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    importance = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = _('regions')
        verbose_name = _('region')
        ordering = ['order']

    def __str__(self):
        return self.name


class Commune(BaseModel):
    # foreign keys

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
    )

    # required fields
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True,
        help_text=_('The name of the commune'),
    )

    class Meta:
        verbose_name_plural = _('communes')
        verbose_name = _('commune')
        ordering = ['name']

    def __str__(self):
        return self.name
