# -*- coding: utf-8 -*-
__author__ = 'yf'
__date__ = '2019/8/31 9:56'

import xadmin
from .models import id_15, lunbo, rewen


class id_5Admin(object):
    list_display = ('id', 'title', 'keywords', 'pub_time')
    search_fields = ('id', 'title', 'keywords')
    list_filter = ('id', 'title', 'keywords')
    ordering = ('-pub_time',)


class lunboAdmin(object):
    list_display = ('id', 'title')
    search_fields = ('id', 'title')
    list_filter = ('id', 'title')


class rewenAdmin(object):
    list_display = ('id', 'title', 'source', 'comment', 'url')
    search_fields = ('id', 'title', 'source', 'comment', 'url')
    list_filter = ('id', 'title', 'source', 'comment', 'url')
    ordering = ('-comment',)


xadmin.site.register(id_15, id_5Admin)
xadmin.site.register(lunbo, lunboAdmin)
xadmin.site.register(rewen, rewenAdmin)
