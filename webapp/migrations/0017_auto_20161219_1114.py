# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_auto_20161219_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='expiry',
            field=models.TimeField(auto_now_add=True),
        ),
    ]