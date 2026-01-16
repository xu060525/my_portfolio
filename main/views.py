from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

from .models import Project
from .forms import ContactForm

# 这里的 request 参数是必须的，代表用户发来的请求
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

            messages.success(request, '邮件已发送！我会尽快回复您。')
            return redirect('contact')  # 提交成功后重定向，防止用户刷新重复提交
        
    else:
        # GET 请求：创建一个空表单
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})