from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from .models import id_15, lunbo, rewen
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext


# Create your views here.


def article_list(request):
    template = get_template('articles.html')
    article_list = id_15.objects.all().order_by('-pub_time')
    lunbo_list = lunbo.objects.all()
    rewen_list = rewen.objects.all().order_by('-comment')[:6]
    paginator = Paginator(article_list, 6)  # 参数1：所有的数据，参数2：每页的记录数
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index', '1')
        # 获取第几页
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(context=locals(), request=request)
    return HttpResponse(html)
    # http://px6tl82gl.bkt.clouddn.com/DevOps%E5%A6%82%E4%BD%95%E5%9C%A8%E4%B8%8D%E7%89%BA%E7%89%B2%E5%AE%89%E5%85%A8%E6%80%A7%E7%9A%84%E6%83%85%E5%86%B5%E4%B8%8B%E8%BF%81%E7%A7%BB%E5%88%B0%E4%BA%91%E7%AB%AF.jpg
    # http://px6tl82gl.bkt.clouddn.com/DevOps%E5%A6%82%E4%BD%95%E5%9C%A8%E4%B8%8D%E7%89%BA%E7%89%B2%E5%AE%89%E5%85%A8%E6%80%A7%E7%9A%84%E6%83%85%E5%86%B5%E4%B8%8B%E8%BF%81%E7%A7%BB%E5%88%B0%E4%BA%91%E7%AB%AF.jpg
