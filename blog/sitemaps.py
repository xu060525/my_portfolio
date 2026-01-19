from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly" # 更新频率：每周
    priority = 0.9        # 权重：0.9 (满分1.0)

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_at # 最后修改时间
    
    # 同样，Django 会尝试调用 obj.get_absolute_url()
    # 如果没定义，我们需要去 models.py 加一下，或者在这里覆写 location 方法
    def location(self, obj):
        from django.urls import reverse
        return reverse('blog:post_detail', args=[obj.slug])