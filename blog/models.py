from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="文章标题")
    # 用于URL的友好字符串，比如 /blog/mu-first-post/
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL别名")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    content = models.TextField(verbose_name="正文 (Markdown) ")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "博客文章"
        verbose_name_plural = "博客文章管理"

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
class Comment(models.Model):
    # 关联文章：文章被删，评论也跟着删
    # related_name='comments' 让我们能用post.comments.all() 查评论
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    name = models.CharField(max_length=80, verbose_name="昵称")
    email = models.EmailField(verbose_name="邮箱")  # 仅后台可见，用于链系
    body = models.TextField(verbose_name="评论内容")

    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True) # 审核开关：如果是 False 就不显示
     
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'