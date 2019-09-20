from django.conf.urls import url, include
from django.contrib import admin
from news.views import index, news_add, news_detail, news_delete, news_edit, news_search, news_category, review_add
from articles.views import article_list
import xadmin

urlpatterns = [
    url(r'^$', index),
    url(r'^news_add/$', news_add),
    url(r'^news_detail/news_id=(\d+)$', news_detail),
    url(r'^news_delete/news_id=(\d+)$', news_delete),
    url(r'^news_edit/news_id=(\d+)$', news_edit),
    url(r'^news_category/category_id=(\d+)$', news_category),
    url(r'^articles_list/marker_id=(\w+)$', article_list),
    url(r'mdeditor/', include('mdeditor.urls')),
    url(r'zonghe/', index),
    url(r'^news_search/$', news_search),
    url(r'^review_add/news_id=(\d+)$', review_add),
    url(r'^login/', xadmin.site.urls),
    url(r'^admin/', admin.site.urls),
]
