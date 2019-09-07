from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'
    verbose_name = '文章管理'   #下一步还需要到init文件中注册一下