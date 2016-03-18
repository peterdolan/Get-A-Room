# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-18 02:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0007_reservation_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='member_requests',
            field=models.ManyToManyField(related_name='group_requests', to='booker.UserProfile'),
        ),
        migrations.AlterField(
            model_name='group',
            name='admins',
            field=models.ManyToManyField(related_name='admin_of', to='booker.UserProfile'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booker.UserProfile'),
        ),
    ]
