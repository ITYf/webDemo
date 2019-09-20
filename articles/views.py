from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from .models import rewen, id_1708, id_519, id_481, id_583, id_15
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.


def article_list(request, id):
    template = get_template('articles.html')
    # 第一条热文不进行排序，一般是特大政治新闻
    rw = rewen.objects.first()
    rewen_list = rewen.objects.all().order_by('-comment')[1:7]

    '''
    由于从前端URL中获取过来的参数是str类型的，
    而每一个表对应的模型是django.db.models.base.ModelBase类型的，
    所有要转换成字符串，截取之后进行比较
    id_1708, id_519, id_481, id_583, id_15
    这里只要截取最后两位数字比较就行，如有重复，截取三位
    '''
    for articles_id in [id_1708, id_519, id_481, id_583, id_15]:
        # print(type(articles_id))
        # print(str(articles_id)[-4:-2])
        if str(articles_id)[-4:-2] == id[-2:]:
            article_list = articles_id.objects.all().order_by('-pub_time')[4:60]
            lunbo_list = articles_id.objects.all().order_by('-pub_time')[:4]
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



