# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-09 06:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0006_group_nres'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booker.Group'),
        ),
    ]