from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # 新增详情页路由
    # <int:project_id> 是一个变量，它会捕获 URL 里的数字，传给视图函数
    path('project/<int:project_id>/', views.detail, name='detail'), 
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]