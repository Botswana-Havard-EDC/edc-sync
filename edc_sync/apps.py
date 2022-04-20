import sys

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.core.management.color import color_style

from .site_sync_models import site_sync_models

style = color_style()


class SyncConfigError(Exception):
    pass


class AppConfig(DjangoAppConfig):
    name = 'edc_sync'
    verbose_name = 'Data Synchronization'
    base_template_name = 'edc_base/base.html'
    custom_json_parsers = []
    server_ip = settings.EDC_SYNC_SERVER_IP
    edc_sync_files_using = True
    update_models=False

    # see edc_device for ROLE

    def ready(self):
        from .signals import (
            serialize_on_post_delete,
            serialize_m2m_on_save, serialize_on_save)
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        site_sync_models.autodiscover()
        sys.stdout.write(' Done loading {}.\n'.format(self.verbose_name))
