# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-22 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0004_auto_20160215_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='vso',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='booker/static/images/profile_images'),
        ),
    ]