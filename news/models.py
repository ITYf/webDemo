from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField

# Create your models here.

class Category(models.Model):
    category_id = models.AutoField(primary_key=True, verbose_name='类别ID')
    name = models.CharField(max_length=10, null=False, verbose_name='类别名')

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Users(models.Model):
    user_id = models.AutoField(primary_key=True, verbose_name='用户ID')
    name = models.CharField(max_length=20, null=False, verbose_name='用户名')
    email = models.EmailField(max_length=40, verbose_name='邮箱')
    password = models.CharField(max_length=32, verbose_name='密码')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class News(models.Model):
    news_id = models.AutoField(primary_key=True, verbose_name='文章ID')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='类别')
    title = models.CharField(max_length=20, null=False, verbose_name='标题')
    content = MDTextField(verbose_name='内容')
    publish_time = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    clicked = models.PositiveIntegerField(verbose_name='点击数', default=0)
    attachment = models.FileField(max_length=100, verbose_name='封面图片')
    enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Review(models.Model):
    review_id = models.AutoField(primary_key=True, verbose_name='评论ID')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='评论文章')
    content = models.TextField(verbose_name='内容')
    publish_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    ip = models.GenericIPAddressField(verbose_name='IP地址')
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
