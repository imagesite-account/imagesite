# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='viewdata',
            old_name='extra_1',
            new_name='labels',
        ),
        migrations.AddField(
            model_name='viewdata',
            name='num_labels',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_0',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_5',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_6',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_7',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_8',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='rating_9',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewdata',
            name='version',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
