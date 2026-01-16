from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Project

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