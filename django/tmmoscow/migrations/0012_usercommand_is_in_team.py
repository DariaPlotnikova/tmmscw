# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-19 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tmmoscow', '0011_auto_20171203_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercommand',
            name='is_in_team',
            field=models.BooleanField(default=False, verbose_name='\u0417\u0430\u043f\u0440\u043e\u0441 \u0441\u0442\u0430\u0442\u044c \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u043e\u043c'),
        ),
    ]