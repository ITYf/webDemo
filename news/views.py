from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from news.models import Category, Users, News, Review
from articles.models import rewen
from news.forms import NewsAddModelForm, ReviewModelForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import markdown


# Create your views here.

def index(request, pid=None, del_pass=None):
    template = get_template('index.html')
    # 第一条热文放第一，一般是特大政治新闻
    rw = rewen.objects.first()
    rewen_list = rewen.objects.all().order_by('-comment')[1:7]

    '''
    导航栏实现
    构造一个字典，循环遍历云计算、移动开发、系统、网络、数据科学
    '''
    cto_dic = {'云计算': 'id_15', '移动开发': 'id_583', '系统': 'id_519', '网络': 'id_481', '数据科学': 'id_1708'}

    # 接受警告框传过来的message
    messages.get_messages(request)

    # 查询出管理员审核通过的信息，按最新时间取前30条文章信息
    news_list = News.objects.filter(enabled=True).order_by('-publish_time')[:30]
    '''
    首页实现分页，这里借助Django的分页器Paginator实现，
    要导入Paginator, PageNotAnInteger, EmptyPage
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象
    
    # has_next              是否有下一页
    # next_page_number      下一页页码
    # has_previous          是否有上一页
    # previous_page_number  上一页页码
    # object_list           分页之后的数据列表
    # number                当前页
    # paginator             paginator对象
    '''
    paginator = Paginator(news_list, 6)  # 参数1：所有的数据，参数2：每页的记录数
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

    categories = Category.objects.all()
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(context=locals(), request=request)
    return HttpResponse(html)


def news_category(request, category_id):
    template = get_template('index.html')
    news_list = News.objects.filter(enabled=True, category__category_id=category_id).order_by('-publish_time')[:30]
    paginator = Paginator(news_list, 6)  # 参数1：所有的数据，参数2：每页的记录数
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index', '1')
        # 获取第几页
        '''
        这里一定要注意，
        为了避免冗余，
        这里采用和index视图中的分页器共用一套模板(本项目中所有视图函数中的分页器都用一套模板)，
        所以对象名必须用number'''
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)
    html = template.render(locals())
    return HttpResponse(html)


def news_add(request):
    if request.method == 'POST':
        '''
        每创建一条记录时，
        字段都要填写完整，
        这里由于用户模块还没完善，
        所以写死了user_id=1,
        并把此实例传给表单保存
        '''
        user = Users.objects.get(user_id=1)
        news = News(user=user)
        # 这里有上传文件的功能，所以可用request.FILES代替request.POST
        form = NewsAddModelForm(request.POST or None, request.FILES or None, instance=news)
        if form.is_valid():
            form.save()
            print('success')
            messages.add_message(request, messages.SUCCESS, '文章发布成功，等待管理员审核！')
            return redirect('/')
        else:
            messages.add_message(request, messages.WARNING, '检查您输入的信息是否正确！')
    else:
        form = NewsAddModelForm()
        messages.add_message(request, messages.WARNING, '如果要发布信息，那么每一个字段都要填写...')
    template = get_template('news_add.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)


def news_detail(request, news_id):
    template = get_template('news_detail.html')
    form = ReviewModelForm()
    try:
        news = News.objects.get(news_id=news_id)
        news.content = markdown.markdown(news.content, extensions=[
            'markdown.extensions.codehilite',
            'markdown.extensions.extra',
            'markdown.extensions.toc',
        ])
        news.clicked += 1
        news.save()
        if news != None:
            reviews = Review.objects.filter(news=news, status=True).order_by('-publish_time')[:30]
            request_context = RequestContext(request)
            request_context.push(locals())
            html = template.render(context=locals(), request=request)
            return HttpResponse(html)
    except:
        return redirect('/')


def news_delete(requests, news_id):
    template = get_template('index.html')
    try:
        news = News.objects.get(news_id=news_id)
        if news != None:
            News.objects.get(news_id=news_id).delete()
            html = template.render(locals())
            return redirect('/')
    except:
        return redirect('/')


def news_edit(request, news_id):
    news = News.objects.get(news_id=news_id)
    if request.method == 'POST':
        form = NewsAddModelForm(request.POST or None, request.FILES or None, instance=news, )
        if form.is_valid():
            form.save()
            '''
            执行form.save()操作将我们的修改保存，
            修改之后的内容还需要管理员审核通过才能显示，
            所以将本条记录的"enabled"字段置为False
            '''
            News.objects.filter(news_id=news_id).update(enabled=False)
            print('success')
            messages.add_message(request, messages.SUCCESS, '文章修改成功，等待管理员审核！')
            return redirect('/')
        else:
            messages.add_message(request, messages.WARNING, '检查您输入的信息是否正确！')
    else:

        form = NewsAddModelForm(
            initial={'title': news.title, 'content': news.content, 'category': news.category,
                     'attachment': news.attachment}
        )
        messages.add_message(request, messages.WARNING, '如果要发布信息，那么每一个字段都要填写...')
    template = get_template('news_edit.html')
    request_context = RequestContext(request)
    request_context.push(context=locals(), request=request)
    html = template.render(request_context)

    return HttpResponse(html)


# 构造模糊查询视图，当在搜索输入框中输入关键字时，匹配标题和关键词相同的文章
def news_search(request):
    keyword = request.GET.get('search')
    if not keyword:
        messages.add_message(request, messages.WARNING, '请输入搜索关键字')
        return redirect('/')
    '''
    这里在用filter()查询时，要加上enabled=True
    否则审核没有通过的文章也会显示
    '''
    news_results = News.objects.filter(enabled=True, title__icontains=keyword).order_by('-publish_time')[:30]
    paginator = Paginator(news_results, 6)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index', '1')
        '''这里一定要注意，查询出来的结果我们也要分页显示，为了避免冗余，这里采用和index视图中的分页器共用一套模板，所以对象名必须用number'''
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)
    template = get_template('index.html')
    html = template.render(locals())
    return HttpResponse(html)


def review_add(request, news_id):
    if request.method == 'POST':
        user = Users.objects.get(user_id=1)
        news = News.objects.get(news_id=news_id)
        '''
        这里使用request对象来获取IP地址，
        考虑到以后网站服务器会使用ngix等代理http，
        或者是该网站做了负载均衡，
        导致使用remote_addr抓取到的是1270.0.1，这时使用HTTP_X_FORWARDED_FOR才获得是用户的真实IP。
        '''
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        review = Review(user=user, news=news, ip=ip)
        form = ReviewModelForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            print('success')
            messages.add_message(request, messages.SUCCESS, '评论发布成功，等待管理员审核！')
            return redirect('/news_detail/news_id=' + news_id)
        else:
            messages.add_message(request, messages.WARNING, '检查您输入的信息是否正确！')
    else:
        form = ReviewModelForm()
    template = get_template('news_detail.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(context=locals(), request=request)
    return HttpResponse(html)
