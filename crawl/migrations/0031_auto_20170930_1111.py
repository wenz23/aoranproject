# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 18:11
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0030_instagrammap_project_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagrammap',
            name='ins_growth',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, db_index=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='instagrammap',
            name='ins_growth_meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='instagrammap',
            name='ins_tags',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, db_index=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='instagrammap',
            name='project_info',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='instagramtracking',
            name='ins_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='instagramtracking',
            name='ins_recent_12_meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]