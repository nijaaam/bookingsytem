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
                ('booking_ref', models.IntegerField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='rooms',
            fields=[
                ('room_id', models.IntegerField(serialize=False, primary_key=True)),
                ('room_name', models.CharField(max_length=60)),
                ('room_size', models.IntegerField()),
                ('room_location', models.TextField()),
                ('room_avaliability', models.TextField()),
                ('room_features', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='bookings',
            name='room_id',
            field=models.ForeignKey(to='webapp.rooms'),
        ),
    ]
