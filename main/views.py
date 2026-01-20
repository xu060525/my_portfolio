import logging

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .models import Project, Tag
from .forms import ContactForm
from blog.models import Post

logger = logging.getLogger(__name__)

# 这里的 request 参数是必须的，代表用户发来的请求
# 加上缓存，有效期15分钟
@cache_page(60 * 15)
@vary_on_cookie
def home(request):
    # 查询所有项目对象
    projects = Project.objects.all()

    # 把数据封装在字典里传给模板
    context = {
        'projects': projects
    }

    # 这里的路径是从 templates 文件夹内部开始算的
    return render(request, 'main/home.html', context)

# 注意这里多了一个参数 project_id，它来自 URL
def detail(request, project_id):
    # 尝试获取项目，如果找不到 ID=999 的项目，自动报 404 错误页面，而不是让程序崩溃
    project = get_object_or_404(Project, pk=project_id)
    
    return render(request, 'main/detail.html', {'project': project})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method =='POST':
        # 用户提交了数据，将数据绑定到表单
        form = ContactForm(request.POST)

        # 验证数据是否合法
        if form.is_valid():
            try:
                # 提取清洗后的数据
                name = form.cleaned_data['name']
                visitor_email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']

                # 组装邮件内容
                full_message = f"【来自网站的留言】\n\n发件人: {name} ({visitor_email})\n\n留言内容:\n{message}"
                
                # 发送邮件函数 (Subject, Message, From, To)
                send_mail(
                    subject=f"【MyWebsite】{subject}",
                    message=full_message,
                    from_email=settings.EMAIL_HOST_USER, # 发件人（占位）
                    recipient_list=['2377392781@qq.com'], # 收件人：填你自己的邮箱
                )
                logger.info("Contact email sent successfully")
            except Exception as e:
                logger.error("Failed to send contact email", exc_info=True)

            messages.success(request, '邮件已发送！我会尽快回复您。')
            return redirect('contact')  # 提交成功后重定向，防止用户刷新重复提交
        
    else:
        # GET 请求：创建一个空表单
        form = ContactForm()
        logger.warning("Invalid contact form submission")

    return render(request, 'main/contact.html', {'form': form})

def project_list(request):
    projects = Project.objects.all()
    tags = Tag.objects.all()

    tag = request.GET.get('tag')
    search_query = request.GET.get('q', '')

    logger.info("Project list visited")
    logger.info(f"Search query='{search_query}', tag='{tag}'")

    if len(search_query) > 50:
        logger.warning("Search query too long")

    # 搜索：标题 or 描述
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Tag 筛选（假设 tag 用 slug）
    if tag:
        projects = projects.filter(
            tags__slug=tag
        )

    projects = projects.distinct()

    context = {
        'projects': projects,
        'tags': tags,
        'tag': tag,
        'search_query': search_query,
    }

    return render(request, 'main/project_list.html', context)

def search(request):
    query = request.GET.get('q')    # 获取 URL 中的 ?q=...

    project_results = []
    post_results = []

    if query:
        # 搜项目：标题 OR 描述 包含关键词
        project_results = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        # 搜博客：标题 OR 正文 包含关键词
        post_results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

        context = {
            'query': query,
            'projects': project_results,
            'posts': post_results, 
        }

        return render(request, 'main/search_results.html', context)

@cache_page(60 * 5)    
def about(request):
    # 技能数据：名称, 熟练度(0-100), 颜色
    skills_data = [
        {"name": "Python/Django", "score": 90, "color": "rgba(255, 99, 132, 0.2)", "border": "rgba(255, 99, 132, 1)"},
        {"name": "C/Embedded", "score": 75, "color": "rgba(54, 162, 235, 0.2)", "border": "rgba(54, 162, 235, 1)"},
        {"name": "Linux/Git", "score": 80, "color": "rgba(255, 206, 86, 0.2)", "border": "rgba(255, 206, 86, 1)"},
        {"name": "ROS/Robot", "score": 70, "color": "rgba(75, 192, 192, 0.2)", "border": "rgba(75, 192, 192, 1)"},
        {"name": "PCB Design", "score": 60, "color": "rgba(153, 102, 255, 0.2)", "border": "rgba(153, 102, 255, 1)"},
    ]
    
    # 提取出 JS 需要的纯列表
    skill_names = [s['name'] for s in skills_data]
    skill_scores = [s['score'] for s in skills_data]
    
    context = {
        'skill_names': skill_names,
        'skill_scores': skill_scores,
    }
    return render(request, 'main/about.html', context)