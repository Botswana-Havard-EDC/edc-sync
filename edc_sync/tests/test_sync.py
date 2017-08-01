from django.apps import apps as django_apps
from django.core.exceptions import MultipleObjectsReturned
from django.test import TestCase, tag
from django.test.utils import override_settings

from edc_sync.models import OutgoingTransaction

from ..constants import INSERT, UPDATE
from ..site_sync_models import site_sync_models
from ..sync_model import SyncHistoricalManagerError, SyncUuidPrimaryKeyMissing
from ..sync_model import SyncModel
from ..sync_model import SyncNaturalKeyMissing, SyncGetByNaturalKeyMissing
from .models import TestModel, BadTestModel, AnotherBadTestModel, YetAnotherBadTestModel
from .models import TestSyncModelNoHistoryManager, TestSyncModelNoUuid

Crypt = django_apps.get_app_config('django_crypto_fields').model

edc_device_app_config = django_apps.get_app_config('edc_device')


class TestSync(TestCase):

    multi_db = True

    def setUp(self):
        site_sync_models.registry = {}
        site_sync_models.loaded = False
        sync_models = ['edc_sync.testmodel',
                       'edc_sync.badtestmodel',
                       'edc_sync.anotherbadtestmodel',
                       'edc_sync.yetanotherbadtestmodel',
                       'edc_sync.testmodelwithfkprotected',
                       'edc_sync.testmodelwithm2m',
                       'edc_sync.testsyncmodelnohistorymanager',
                       'edc_sync.testsyncmodelnouuid']
        site_sync_models.register(sync_models, SyncModel)

    def get_credentials(self):
        return self.create_apikey(username=self.username,
                                  api_key=self.api_client_key)

    def test_str(self):
        obj = TestModel()
        obj = SyncModel(obj)
        self.assertTrue(str(obj))
        self.assertTrue(repr(obj))

    def test_raises_on_missing_natural_key(self):
        with override_settings(DEVICE_ID='10'):
            with self.assertRaises(SyncNaturalKeyMissing):
                BadTestModel.objects.using('client').create()

    def test_raises_on_missing_get_by_natural_key(self):
        with override_settings(DEVICE_ID='10'):
            with self.assertRaises(SyncGetByNaturalKeyMissing):
                AnotherBadTestModel.objects.using('client').create()

    def test_raises_on_wrong_type_of_historical_manager(self):
        with override_settings(DEVICE_ID='10'):
            with self.assertRaises(SyncHistoricalManagerError):
                YetAnotherBadTestModel.objects.using('client').create()

    def test_raises_on_no_historical_manager(self):
        with override_settings(DEVICE_ID='10'):
            try:
                TestSyncModelNoHistoryManager.objects.using('client').create()
            except SyncHistoricalManagerError:
                self.fail('SyncHistoricalManagerError unexpectedly raised.')

    def test_raises_on_missing_uuid_primary_key(self):
        with override_settings(DEVICE_ID='10'):
            with self.assertRaises(SyncUuidPrimaryKeyMissing):
                TestSyncModelNoUuid.objects.using('client').create()

    def test_creates_outgoing_on_add(self):
        with override_settings(DEVICE_ID='10'):
            test_model = TestModel.objects.using('client').create(f1='erik')
            with self.assertRaises(OutgoingTransaction.DoesNotExist):
                try:
                    OutgoingTransaction.objects.using('client').get(
                        tx_pk=test_model.pk,
                        tx_name='edc_sync.testmodel',
                        action=INSERT)
                except OutgoingTransaction.DoesNotExist:
                    pass
                else:
                    raise OutgoingTransaction.DoesNotExist()
            history_obj = test_model.history.using(
                'client').get(id=test_model.id)
            with self.assertRaises(OutgoingTransaction.DoesNotExist):
                try:
                    OutgoingTransaction.objects.using('client').get(
                        tx_pk=history_obj.history_id,
                        tx_name='edc_sync.historicaltestmodel',
                        action=INSERT)
                except OutgoingTransaction.DoesNotExist:
                    pass
                else:
                    raise OutgoingTransaction.DoesNotExist()

    @override_settings(ALLOW_MODEL_SERIALIZATION=False)
    def test_does_not_create_outgoing(self):
        with override_settings(DEVICE_ID='10', ALLOW_MODEL_SERIALIZATION=False):
            test_model = TestModel.objects.using('client').create(f1='erik')
            with self.assertRaises(OutgoingTransaction.DoesNotExist):
                OutgoingTransaction.objects.using(
                    'client').get(tx_pk=test_model.pk)

    def test_creates_outgoing_on_change(self):
        with override_settings(DEVICE_ID='10'):
            test_model = TestModel.objects.using('client').create(f1='erik')
            test_model.save(using='client')
            with self.assertRaises(OutgoingTransaction.DoesNotExist):
                try:
                    OutgoingTransaction.objects.using('client').get(
                        tx_pk=test_model.pk,
                        tx_name='edc_sync.testmodel',
                        action=INSERT)
                    OutgoingTransaction.objects.using('client').get(
                        tx_pk=test_model.pk,
                        tx_name='edc_sync.testmodel',
                        action=UPDATE)
                except OutgoingTransaction.DoesNotExist:
                    pass
                else:
                    raise OutgoingTransaction.DoesNotExist()
            self.assertEqual(
                2, OutgoingTransaction.objects.using('client').filter(
                    tx_name='edc_sync.historicaltestmodel',
                    action=INSERT).count())

    def test_timestamp_is_default_order(self):
        with override_settings(DEVICE_ID='10'):
            test_model = TestModel.objects.using('client').create(f1='erik')
            test_model.save(using='client')
            last = 0
            for obj in OutgoingTransaction.objects.using('client').all():
                self.assertGreaterEqual(int(obj.timestamp), last)
                last = int(obj.timestamp)

    def test_created_obj_serializes_to_correct_db(self):
        """Asserts that the obj and the audit obj serialize to the
        correct DB in a multi-database environment.
        """
        TestModel.objects.using('client').create(f1='erik')
        result = [
            obj.tx_name for obj in OutgoingTransaction.objects.using('client').all()]
        result.sort()
        self.assertListEqual(
            result,
            ['edc_sync.historicaltestmodel', 'edc_sync.testmodel'])
        self.assertListEqual(
            [obj.tx_name for obj in OutgoingTransaction.objects.using('server').all()], [])
        self.assertRaises(
            OutgoingTransaction.DoesNotExist,
            OutgoingTransaction.objects.using('server').get,
            tx_name='edc_sync.testmodel')
        self.assertRaises(
            MultipleObjectsReturned,
            OutgoingTransaction.objects.using('client').get,
            tx_name__contains='testmodel')

    def test_updated_obj_serializes_to_correct_db(self):
        """Asserts that the obj and the audit obj serialize to the
        correct DB in a multi-database environment.
        """
        test_model = TestModel.objects.using('client').create(f1='erik')
        result = [obj.tx_name for obj in OutgoingTransaction.objects.using(
            'client').filter(action=INSERT)]
        result.sort()
        self.assertListEqual(
            result, ['edc_sync.historicaltestmodel',
                     'edc_sync.testmodel'])
        self.assertListEqual(
            [obj.tx_name for obj in OutgoingTransaction.objects.using(
                'client').filter(action=UPDATE)],
            [])
        test_model.save(using='client')
        self.assertListEqual(
            [obj.tx_name for obj in OutgoingTransaction.objects.using(
                'client').filter(action=UPDATE)],
            [u'edc_sync.testmodel'])
        result = [obj.tx_name for obj in OutgoingTransaction.objects.using(
            'client').filter(action=INSERT)]
        result.sort()
        self.assertListEqual(
            result,
            ['edc_sync.historicaltestmodel',
             'edc_sync.historicaltestmodel',
             'edc_sync.testmodel'])
