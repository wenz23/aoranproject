# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 18:26
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0034_auto_20171025_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='googlemap',
            name='query',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
