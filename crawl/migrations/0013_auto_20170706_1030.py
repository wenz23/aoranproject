# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-06 17:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0012_auto_20170705_1943'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SocialDetails',
            new_name='YouTubeDetails',
        ),
    ]
