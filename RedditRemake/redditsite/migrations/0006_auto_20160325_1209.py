# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 19:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('redditsite', '0005_auto_20160325_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('direction', models.CharField(choices=[('U', 'Up'), ('D', 'Down')], max_length=4)),
                ('commment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='redditsite.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='PostVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('direction', models.CharField(choices=[('U', 'Up'), ('D', 'Down')], max_length=4)),
            ],
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, help_text='optional', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='postvote',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='redditsite.Post'),
        ),
    ]
