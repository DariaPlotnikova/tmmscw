# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-17 23:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tmmoscow', '0007_auto_20171117_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercommand',
            name='user',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]