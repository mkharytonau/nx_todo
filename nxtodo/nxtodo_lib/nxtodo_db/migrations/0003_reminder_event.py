# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-22 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nxtodo_db', '0002_remove_reminder_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='event',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='nxtodo_db.Event'),
            preserve_default=False,
        ),
    ]
