from base.middleware import RequestMiddleware
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from base.utils import get_our_models


@receiver(post_save)
def audit_log(sender, instance, created, raw, update_fields, **kwargs):
    # Lista de los modelos que se requienran que escuche
    if sender not in get_our_models():
        return

    sensitive_fields = ['password', ]

    user = get_user()

    if created:
        message = []
        message.append({'Created': instance.to_dict(
                exclude=['created_at', 'updated_at', 'original_dict', 'id'],
                include_m2m=True,
        )})
        instance.save_addition(user, message)
    elif not raw:
        change_message = []
        changed_field_labels = {}
        original_dict = instance.original_dict
        actual_dict = instance.to_dict(
                exclude=['created_at', 'updated_at', 'original_dict', 'id'],
                include_m2m=False,
        )

        for key in original_dict.keys():
            if original_dict[key] != actual_dict[key]:
                if key == sensitive_fields:
                    changed_field_labels[key] = {'change': 'field updated'}
                else:
                    changed_field_labels[key] = {
                        'from': original_dict[key],
                        'to': actual_dict[key],
                    }

        change_message.append({'changed': {'fields': changed_field_labels}})
        instance.save_edition(user, change_message)


@receiver(post_delete)
def audit_delete_log(sender, instance, **kwargs):
    # Lista de los modelos que se requienran que escuche
    if sender not in get_our_models():
        return
    user = get_user()
    instance.save_deletion(user)


def get_user():
    thread_local = RequestMiddleware.thread_local
    if hasattr(thread_local, 'user'):
        user = thread_local.user
    else:
        user = None

    return user
