# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-24 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kilogram', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='thumbnail_image',
        ),
        migrations.AddField(
            model_name='photo',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]