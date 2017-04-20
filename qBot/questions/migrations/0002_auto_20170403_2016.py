# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-04-03 18:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='user_votes_down',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user_votes_up',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='answer',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='pinned_by',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='is_made_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
