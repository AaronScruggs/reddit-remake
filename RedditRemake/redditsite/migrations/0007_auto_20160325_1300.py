# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 20:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redditsite', '0006_auto_20160325_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentvote',
            old_name='commment',
            new_name='comment',
        ),
    ]
