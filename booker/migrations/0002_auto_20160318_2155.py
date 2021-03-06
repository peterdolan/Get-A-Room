# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-18 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='member_requests',
            field=models.ManyToManyField(null=True, related_name='group_requests', to='booker.UserProfile'),
        ),
        migrations.AlterField(
            model_name='group',
            name='admins',
            field=models.ManyToManyField(related_name='admin_of', to='booker.UserProfile'),
        ),
    ]
