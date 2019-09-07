# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-08-31 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20190831_0942'),
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
        migrations.AlterField(
            model_name='review',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.News', verbose_name='评论文章'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Users', verbose_name='用户'),
        ),
    ]
