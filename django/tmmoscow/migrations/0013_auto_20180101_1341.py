# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-01 13:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tmmoscow', '0012_usercommand_is_in_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='distances', to='tmmoscow.Distance', verbose_name='\u0414\u0438\u0441\u0442\u0430\u043d\u0446\u0438\u044f')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='distances', to=settings.AUTH_USER_MODEL, verbose_name='\u0423\u0447\u0430\u0441\u0442\u0438\u043a')),
            ],
        ),
        migrations.AlterField(
            model_name='usercommand',
            name='is_in_team',
            field=models.BooleanField(default=False, verbose_name='\u0412 \u043a\u043e\u043c\u0430\u043d\u0434\u0435'),
        ),
    ]
