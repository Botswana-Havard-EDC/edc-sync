from datetime import datetime

from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core import serializers
# from django.db.models import get_model
from django.apps import apps

# from edc.core.crypto_fields.classes import FieldCryptor
from django_crypto_fields.classes import Cryptor

from sync_old import Transaction, transaction_producer

from sync_old import BaseSyncUuidModel
from sync_old import IncomingTransaction


@receiver(post_save, weak=False, dispatch_uid="deserialize_to_inspector_on_post_save")
def deserialize_to_inspector_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        try:
            # method only exists on MiddleManTransaction
            instance.deserialize_to_inspector_on_post_save(instance, raw, created, using, **kwargs)
        except AttributeError as attribute_error:
            if 'deserialize_to_inspector_on_post_save' in str(attribute_error):
                pass
            else:
                raise


@receiver(m2m_changed, weak=False, dispatch_uid='serialize_m2m_on_save')
def serialize_m2m_on_save(sender, action, instance, using, **kwargs):
    """ Part of the serialize transaction process that ensures m2m are
    serialized correctly.
    """
    if action == 'post_add':
        if isinstance(instance, BaseSyncUuidModel):
            if instance.is_serialized() or instance._meta.proxy:
                transaction = Transaction()
                # default raw to False, created to True
                # TODO: serialize is skipped if raw is True, how should raw
                # affect serialization of m2m?
                # https://docs.djangoproject.com/en/dev/ref/signals/#m2m-changed
                raw = False
                created = True
                transaction.serialize(sender, instance, raw, created, using, **kwargs)


@receiver(post_save, weak=False, dispatch_uid='serialize_on_save')
def serialize_on_save(sender, instance, raw, created, using, **kwargs):
    """ Serialize the model instance as an OutgoingTransaction."""
    if not raw:
        if isinstance(instance, BaseSyncUuidModel):
            if instance.is_serialized() or instance._meta.proxy:
                transaction = Transaction()
                transaction.serialize(sender, instance, raw, created, using, **kwargs)


@receiver(post_save, sender=IncomingTransaction, dispatch_uid="deserialize_on_post_save")
def deserialize_on_post_save(sender, instance, raw, created, using, **kwargs):
    pass
    """ Callback to deserialize an incoming transaction.

    as long as the transaction is not consumed or in error"""


@receiver(post_delete, weak=False, dispatch_uid="serialize_on_post_delete")
def serialize_on_post_delete(sender, instance, using, **kwargs):
    """Creates an serialized OutgoingTransaction when a model instance is deleted."""
    using = using or 'default'
    try:
        is_serialized = instance.is_serialized()
    except AttributeError:
        pass
    if is_serialized or instance._meta.proxy:
        transaction = Transaction(instance)

        
        OutgoingTransaction = apps.get_model('sync_old', 'outgoingtransaction')
        json_obj = serializers.serialize(
            "json", [instance, ],
            ensure_ascii=False,
            use_natural_keys=True)
        json_tx = Cryptor().aes_encrypt(json_obj, 'local')
        OutgoingTransaction.objects.using(using).create(
            tx_name=instance._meta.object_name,
            tx_pk=instance.pk,
            tx=json_tx,
            timestamp=datetime.today().strftime('%Y%m%d%H%M%S%f'),
            producer=transaction_producer,
            action='D')