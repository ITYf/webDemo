from django.db import models


# Create your models here.

class id_15(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='文章ID')
    title = models.CharField(max_length=60, null=False, verbose_name='文章标题')
    keywords = models.CharField(max_length=30, null=False, verbose_name='文章关键词')
    pub_time = models.DateTimeField(verbose_name='发布时间')
    img_url = models.URLField(verbose_name='封面URL')
    url = models.URLField(verbose_name='详情链接')

    class Meta():
        verbose_name = '博文详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class lunbo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='文章ID')
    title = models.CharField(max_length=40, null=False, verbose_name='文章标题')
    img = models.TextField(verbose_name='封面URL')
    url = models.TextField(verbose_name='详情链接')

    class Meta():
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class rewen(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='热文ID')
    title = models.CharField(max_length=40, null=False, verbose_name='热文标题')
    source = models.CharField(max_length=20, verbose_name='热文来源')
    comment = models.IntegerField(verbose_name='评论数量')
    url = models.URLField(verbose_name='详情链接')

    class Meta:
        verbose_name = '头条热文'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
