# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bookings',
            fields=[
                ('booking_ref', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('contact', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='recurringBookings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('recurence', models.CharField(choices=[(b'1', b'Daily'), (b'2', b'Weekly'), (b'3', b'Biweekly')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='reservations',
            fields=[
                ('reservations_id', models.AutoField(primary_key=True, serialize=False)),
                ('expiry', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='rooms',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=60)),
                ('room_size', models.IntegerField()),
                ('room_location', models.TextField()),
                ('room_features', models.TextField()),
                ('in_use', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='reservations',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bksys.rooms'),
        ),
        migrations.AddField(
            model_name='recurringbookings',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bksys.rooms'),
        ),
        migrations.AddField(
            model_name='bookings',
            name='recurrence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bksys.recurringBookings'),
        ),
        migrations.AddField(
            model_name='bookings',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bksys.rooms'),
        ),
    ]
