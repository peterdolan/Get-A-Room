# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-09 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0005_auto_20160222_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='nres',
            field=models.PositiveSmallIntegerField(default=20),
        ),
    ]