# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bookings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('booking_ref', models.CharField(max_length=60)),
                ('room_id', models.IntegerField()),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='rooms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('room_id', models.IntegerField()),
                ('room_name', models.CharField(max_length=60)),
                ('room_size', models.IntegerField()),
                ('room_location', models.TextField()),
                ('room_features', models.TextField()),
            ],
        ),
    ]
