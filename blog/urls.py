from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'   # 命名空间，以后用 {% url 'blog:detail' %} 引用

urlpatterns = [
    path('', views.post_list, name='list'),

    path('like/', views.like_post, name='like_post'), 
    path('feed/', LatestPostsFeed(), name='post_feed'),
    # 一定要将通用的放在最后，特殊的放在前面
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]