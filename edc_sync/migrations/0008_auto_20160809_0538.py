# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-09 03:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edc_sync', '0007_auto_20160807_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='archive_path',
        ),
        migrations.RemoveField(
            model_name='history',
            name='filesize',
        ),
        migrations.RemoveField(
            model_name='history',
            name='filetimestamp',
        ),
        migrations.RemoveField(
            model_name='history',
            name='location',
        ),
        migrations.RemoveField(
            model_name='history',
            name='remote_path',
        ),
        migrations.RemoveField(
            model_name='history',
            name='status',
        ),
    ]
