# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-07 05:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0005_auto_20160222_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='organization',
            field=models.ForeignKey(default='ASSU', on_delete=django.db.models.deletion.CASCADE, to='booker.Organization'),
            preserve_default=False,
        ),
    ]