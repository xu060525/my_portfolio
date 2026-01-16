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

    class Meta:
        ordering = ['-created_at']
        verbose_name = "博客文章"
        verbose_name_plural = "博客文章管理"

    def __str__(self):
        return self.title