# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-24 13:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kilogram', '0002_auto_20170724_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='thumnail_image',
            new_name='thumbnail_image',
        ),
    ]