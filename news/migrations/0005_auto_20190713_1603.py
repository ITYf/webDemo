# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-13 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20190713_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Category', verbose_name='类别'),
        ),
        migrations.AlterField(
            model_name='news',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Users', verbose_name='用户'),
        ),
    ]
