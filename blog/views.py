from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
import markdown

from .models import Post

def post_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    
    # 每页显示 5 篇文章
    paginator = Paginator(post_list, 5) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # --- Markdown 渲染核心 ---
    # extensions 解释：
    # 'markdown.extensions.extra': 支持表格、脚注等扩展语法
    # 'markdown.extensions.codehilite': 代码高亮
    # 'markdown.extensions.toc': 自动生成目录
    post.content = markdown.markdown(post.content, extensions=[
        'markdown.extensions.fenced_code',  # 把它放在第一个！
        'markdown.extensions.codehilite',   # 负责高亮
        'markdown.extensions.extra',        # 负责表格等其他杂项
        'markdown.extensions.toc',
    ])
    
    return render(request, 'blog/detail.html', {'post': post})
