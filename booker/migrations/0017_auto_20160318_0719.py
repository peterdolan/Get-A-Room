# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-18 07:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0016_auto_20160318_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='nres',
            field=models.PositiveSmallIntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booker.Room'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booker.UserProfile'),
        ),
    ]
