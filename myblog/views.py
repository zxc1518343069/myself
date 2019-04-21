from django.shortcuts import get_object_or_404,render
from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from comment.models import Comment
from comment.forms import CommentForm



def get_blog_list_commmon_date(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, 5)  # 建立分页对象，参数为博客列表,每页要分的博客数目
    page_num = request.GET.get('page', 1)  # 获取url页码参数，默认取1
    page_of_blogs = paginator.get_page(page_num)  # 返回具体的分页 通过调用该对象的object_list方法可以取得当前分页下所有博客

    current_page_num = page_of_blogs.number  #获取当前页面
    page_range = list(range(max(current_page_num-2,1),current_page_num))+list(range(current_page_num,min(current_page_num + 2,paginator.num_pages)+1))
    if page_range[0]-1 >= 2:
        page_range.insert(0,'...')
    if page_range[0] != 1:
        page_range.insert(0,1)
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    # 获取博客分类对应的博客数量
    blog_types = BlogType.objects.all() #得到全部博客
    blog_types_list = []    #建立一个列表
    for blog_type in blog_types:    #遍历所有博客，
        blog_type.blog_count = Blog.objects.filter(blog_type = blog_type).count()
        blog_types_list.append(blog_type)

    # 获取博客日期对应的数量
    blog_dates = Blog.objects.dates('created_time','month',order='DESC')# 字段 类型 排序
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year = blog_date.year,
                                         created_time__month = blog_date.month).count()
        blog_dates_dict[blog_date] =blog_count

    context = {}
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = blog_types_list
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):

    blogs_all_list = Blog.objects.all()  # 获取博客列表
    context = get_blog_list_commmon_date(request,blogs_all_list)
    return render(request,'blog/blog_list.html',context)

def blog_detail(request,blog_pk):#打开具体某一篇
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_readed' %blog_pk):
        ct = ContentType.objects.get_for_model(Blog)
        if ReadNum.objects.filter(content_type=ct,object_id=blog.pk).count():
            readnum = ReadNum.objects.get(content_type=ct,object_id=blog.pk)
        else:
            readnum = ReadNum(content_type=ct,object_id=blog.pk)

        readnum.read_num += 1
        readnum.save()
    blog_contene_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_contene_type,object_id=blog_pk)

    context = {}  # 创建一个字典
    context['previous_blog'] = Blog.objects.filter(created_time__gt = blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt= blog.created_time).first()
    context['blog'] = blog
    context['comments'] = comments
    context['comment_form'] = CommentForm(initial={'content_type':blog_contene_type.model,
                                                   'object_id':blog_pk})
    response = render(request,'blog/blog_detail.html',context)# 响应
    response.set_cookie('blog_%s_readed' %blog_pk,'ture',max_age=60)  # 60秒有效  ture代表已经访问
    return response #返回一个字典对象，属性市里面有的

def blogs_with_type(request,blog_type_pk):
    blog_type =get_object_or_404(BlogType,pk =blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type_pk)  # 获取博客列表
    context = get_blog_list_commmon_date(request,blogs_all_list)
    context['blog_type'] = blog_type

    return render(request,'blog/blogs_with_date.html', context)

def blogs_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)  # 获取博客列表
    context = get_blog_list_commmon_date(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year,month)
    return render(request,'blog/blogs_with_type.html', context)

# Create your views here.
