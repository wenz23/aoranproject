# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-17 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gyms',
            name='state',
            field=models.CharField(blank=True, db_index=True, max_length=2000, null=True),
        ),
    ]