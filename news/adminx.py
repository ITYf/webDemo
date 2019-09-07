# -*- coding: utf-8 -*-
__author__ = 'yf'
__date__ = '2019/7/9 20:08'

import xadmin
from .models import Category, News, Users, Review
from xadmin import views


class BaseSetting(object):
    pass
    # enable_themes = True   #启用主题，启用之后刷新变慢，因为用的是Google的主题
    # use_bootswatch = True


class GlobalSeeting(object):
    site_title = '猿头条后台管理系统'
    site_footer = '2019年07月13日.猿头条'
    menu_style = 'accordion'  # 收起菜单栏


class categoryAdmin(object):
    list_display = ('category_id', 'name')
    search_fields = ('category_id', 'name')
    list_filter = ('category_id', 'name')


class usersAdmin(object):
    list_display = ('user_id', 'name', 'email', 'password')
    search_fields = ('user_id', 'name', 'email')
    list_filter = ('user_id', 'name', 'email')


class newsAdmin(object):
    list_display = ('news_id', 'user', 'category', 'title', 'publish_time', 'clicked', 'enabled')
    search_fields = ('news_id', 'title')
    list_filter = ('news_id', 'user__name', 'category__name', 'title', 'publish_time', 'clicked', 'enabled')
    ordering = ('-publish_time',)


class reviewAdmin(object):
    list_display = ('review_id', 'user', 'news', 'ip', 'status')
    search_fields = ('news', 'ip', 'user', 'content')
    list_filter = ('news', 'user__name')
    ordering = ('-publish_time',)


xadmin.site.register(Category, categoryAdmin)
xadmin.site.register(Users, usersAdmin)
xadmin.site.register(News, newsAdmin)
xadmin.site.register(Review, reviewAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSeeting)
