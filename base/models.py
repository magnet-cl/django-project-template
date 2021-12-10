""" Models for the base application.

All apps should use the BaseModel as parent for all models
"""

# standard library
import json

# django
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# base
from base import utils
from base.managers import BaseManager
from base.serializers import ModelEncoder
from base.mixins import AuditMixin


# public methods
def file_path(self, name):
    """
    Generic method to give to a FileField or ImageField in it's upload_to
    parameter.

    This returns the name of the class, concatenated with the id of the
    object and the name of the file.
    """
    base_path = "{}/{}/{}/{}"

    return base_path.format(
        self.__class__.__name__,
        str(utils.today()),
        utils.random_string(30),
        name
    )


class BaseModel(AuditMixin, models.Model):
    """ An abstract class that every model should inherit from """
    BOOLEAN_CHOICES = ((False, _('No')), (True, _('Yes')))

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("creation date"),
        verbose_name=_('created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True,
        help_text=_("edition date"),
        verbose_name=_('updated at'),
    )

    # field used to store a dictionary with the instance original fields
    original_dict = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_dict = self.to_dict(
            exclude=settings.LOG_IGNORE_FIELDS,
            include_m2m=False,
        )

    # using BaseManager
    objects = BaseManager()

    class Meta:
        """ set to abstract """
        abstract = True

    # public methods
    def update(self, skip_save=False, **kwargs):
        """
        This is a shortcut method, it basically sets all keyword arguments as
        attributes on the calling object, then it stores only those values
        into the database.

        To store values into the database, this method uses the `save` method
        with the `update_fields` parameter, but if you want to skip the save
        method, you can pass the parameter `skip_save=True` when calling update
        (useful when you want to avoid calling save signals).
        """
        kwargs['updated_at'] = timezone.now()

        for kw in kwargs:
            self.__setattr__(kw, kwargs[kw])

        if skip_save:
            self.__class__.objects.filter(pk=self.pk).update(**kwargs)
        else:
            self.save(update_fields=kwargs.keys())

    def to_dict(instance, fields=None, exclude=None, include_m2m=True):
        """
        Returns a dict containing the data in ``instance``

        ``fields`` is an optional list of field names. If provided, only the
        named fields will be included in the returned dict.

        ``exclude`` is an optional list of field names. If provided, the named
        fields will be excluded from the returned dict, even if they are listed
        in the ``fields`` argument.
        """

        opts = instance._meta
        data = {}
        for f in opts.fields + opts.many_to_many:
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, models.fields.related.ForeignKey):
                data[f.name + '_id'] = f.value_from_object(instance)
            elif isinstance(f, models.fields.related.ManyToManyField):
                if include_m2m:
                    # If the object doesn't have a primary key yet, just use an
                    # emptylist for its m2m fields. Calling f.value_from_object
                    # will raise an exception.
                    if instance.pk is None:
                        data[f.name] = []
                    else:
                        # MultipleChoiceWidget needs a list of pks, not objects
                        data[f.name + '_ids'] = list(
                            getattr(instance, f.attname).values_list(
                                'pk',
                                flat=True
                            )
                        )
            else:
                data[f.name] = f.value_from_object(instance)
        return data

    def to_json(self, fields=None, exclude=None, **kargs):
        """
        Returns a string containing the data in of the instance in json format

        ``fields`` is an optional list of field names. If provided, only the
        named fields will be included in the returned dict.

        ``exclude`` is an optional list of field names. If provided, the named
        fields will be excluded from the returned dict, even if they are listed
        in the ``fields`` argument.

        kwargs are optional named parameters for the json.dumps method
        """
        # obtain a dict of the instance data
        data = self.to_dict(fields=fields, exclude=exclude)

        # turn the dict to json
        return json.dumps(data, cls=ModelEncoder, **kargs)

    def get_full_url(self):
        absolute_url = self.get_absolute_url()
        site = Site.objects.get_current().domain
        return 'http://{site}{path}'.format(site=site, path=absolute_url)


class OrderableModel(BaseModel):
    display_order = models.PositiveSmallIntegerField(
        _('display order'),
        default=0,
    )

    class Meta:
        abstract = True
        ordering = ('display_order',)

    def _set_display_order(self):
        '''
        When adding a new object, set display_order field
        counting all objects plus 1
        '''
        obj_count = self.__class__.objects.count()
        self.display_order = obj_count + 1

    @classmethod
    def reorder_display_order(cls):
        '''
        Take all objects and change order value
        '''
        objects = cls.objects.all()
        order = 0
        for obj in objects:
            obj.display_order = order
            obj.save()
            order += 1

    def save(self, *args, **kwargs):
        if self.pk is None:
            self._set_display_order()
        super().save(*args, **kwargs)
