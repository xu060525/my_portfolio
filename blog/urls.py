from django.urls import path
from . import views

app_name = 'blog'   # 命名空间，以后用 {% url 'blog:detail' %} 引用

urlpatterns = [
    path('', views.post_list, name='list'),
    path('<slug:slug>/', views.post_detail, name='detail'),
]