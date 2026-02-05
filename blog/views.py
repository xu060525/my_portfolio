from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
import markdown

from .models import Post
from .forms import CommentForm
from .serializers import PostSerializer, PostDetailSerializer

def post_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    
    # 每页显示 5 篇文章
    paginator = Paginator(post_list, 5) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    
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

    # 这里的逻辑和 Day 10 的 Contact 类似
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # 暂不保存到数据库，因为还需要关联 post
            new_comment = form.save(commit=False)
            new_comment.post = post # 关联当前文章
            new_comment.save() # 正式保存
            # 刷新页面，防止重复提交
            return redirect('blog:detail', slug=slug)
    else:
        form = CommentForm()
    
    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,         
    })

@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('id')
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'msg': 'Login required'})
    
    post = get_object_or_404(Post, id=post_id)
    
    # 核心逻辑：点过就删，没点就加
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        
    return JsonResponse({
        'status': 'ok', 
        'count': post.likes.count(), 
        'liked': liked # 告诉前端现在的状态
    })

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    # 只显示已发布的文章
    queryset = Post.objects.all().order_by('-created_at')

    # 动态选择 Serializer
    def get_serializer_class(self):
        if self.action == 'retrieve': # 代表详情页 (GET /api/osts/1/)
            return PostDetailSerializer
        return PostSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']    # 允许标题和正文
    
