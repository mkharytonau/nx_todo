# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-16 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nxtodo_db', '0009_delete_reminder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_remind_before', models.TextField()),
                ('start_remind_from', models.TextField()),
                ('stop_in_moment', models.TextField()),
                ('remind_in', models.TextField()),
                ('datetimes', models.TextField()),
                ('interval', models.TextField()),
                ('weekdays', models.TextField()),
                ('parent', models.TextField()),
                ('kind', models.TextField()),
            ],
        ),
    ]
