# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-25 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0026_auto_20170825_1128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagrammap',
            name='latest_visited_at',
        ),
        migrations.AddField(
            model_name='instagrammap',
            name='latest_crawl_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='instagrammap',
            name='latest_similar_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
