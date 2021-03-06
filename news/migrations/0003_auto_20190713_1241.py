# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-13 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20190713_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='news',
            name='attachment',
            field=models.FileField(upload_to='', verbose_name='封面图片'),
        ),
    ]
