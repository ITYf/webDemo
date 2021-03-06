# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-13 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '类别', 'verbose_name_plural': '类别'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AlterField(
            model_name='category',
            name='category_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='类别ID'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=10, verbose_name='类别名'),
        ),
        migrations.AlterField(
            model_name='news',
            name='attachment',
            field=models.CharField(max_length=100, verbose_name='封面图片'),
        ),
        migrations.AlterField(
            model_name='news',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='类别ID'),
        ),
        migrations.AlterField(
            model_name='news',
            name='clicked',
            field=models.PositiveIntegerField(default=0, verbose_name='点击数'),
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='news',
            name='news_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='文章ID'),
        ),
        migrations.AlterField(
            model_name='news',
            name='publish_time',
            field=models.DateTimeField(auto_now=True, verbose_name='发布时间'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=100, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='news',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.users', verbose_name='用户ID'),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=40, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(max_length=20, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=32, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='用户ID'),
        ),
    ]
