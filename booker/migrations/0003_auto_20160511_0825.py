# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-11 08:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0002_auto_20160318_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_group_admin',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_org_admin',
        ),
    ]
