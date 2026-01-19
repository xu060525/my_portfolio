from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse

from .models import Post

class LatestPostsFeed(Feed):
    title = "徐恺翔的博客"
    link = "/blog/"
    description = "关于 Python, Django 和 自动化的技术分享。"

    # 1. 获取要推送的数据（最新的5篇文章）
    def items(self):
        return Post.objects.all().order_by('-created_at')[:5]

    # 2. 数据的标题
    def item_title(self, item):
        return item.title

    # 3. 数据的描述（取前30个词）
    def item_description(self, item):
        return truncatewords(item.content, 30)

    # 4. 数据的链接（Django 会自动调用 item.get_absolute_url()，如果没有定义，需手动写）
    # 假设你的 Post 模型里还没定义 get_absolute_url，我们这里手动指定：
    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.slug])