# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-24 10:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kilogram', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='thumname_image',
            new_name='thumnail_image',
        ),
    ]
