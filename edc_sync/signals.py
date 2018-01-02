from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from edc_base.site_models import SiteModelNotRegistered
from rest_framework.authtoken.models import Token

from .site_sync_models import site_sync_models


@receiver(post_save, sender=Token)
def create_auth_token(sender, instance, raw, created, **kwargs):
    """Create token when a user is created (from rest_framework)."""
    if not raw:
        if created:
            sender.objects.create(user=instance)


@receiver(m2m_changed, weak=False, dispatch_uid='serialize_m2m_on_save')
def serialize_m2m_on_save(sender, action, instance, using, **kwargs):
    """ Part of the serialize transaction process that ensures m2m are
    serialized correctly.
    """
    if action == 'post_add':
        try:
            sync_model = site_sync_models.get_wrapped_instance(instance)
        except SiteModelNotRegistered:
            pass
        else:
            sync_model.to_outgoing_transaction(using, created=True)


@receiver(post_save, weak=False, dispatch_uid='serialize_on_save')
def serialize_on_save(sender, instance, raw, created, using, **kwargs):
    """ Serialize the model instance as an OutgoingTransaction.
    """
    if not raw:
        try:
            sync_model = site_sync_models.get_wrapped_instance(instance)
        except SiteModelNotRegistered:
            pass
        else:
            sync_model.to_outgoing_transaction(using, created=created)


@receiver(post_delete, weak=False, dispatch_uid="serialize_on_post_delete")
def serialize_on_post_delete(sender, instance, using, **kwargs):
    """Creates a serialized OutgoingTransaction when
    a model instance is deleted.
    """
    try:
        sync_model = site_sync_models.get_wrapped_instance(instance)
    except SiteModelNotRegistered:
        pass
    else:
        sync_model.to_outgoing_transaction(using, created=False, deleted=True)
