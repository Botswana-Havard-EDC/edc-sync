# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_sync', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomingtransaction',
            name='tx',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='outgoingtransaction',
            name='tx',
            field=models.BinaryField(),
        ),
    ]