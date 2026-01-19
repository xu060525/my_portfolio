# 我的个人博客项目开发记录

今天我开始开发了我的个人博客，我会把每天干的事情，以及我的思考记录在这里。一边学Django，一边进行开发，做中学，这是我觉得最高效的学习方式。

---

## Day 0: 需求分析与技术选型

作为开始前的准备，我今天应当先搞清楚我要做什么，我为什么要这么做。

---

### 为什么我选择做这个项目？

1. 我可以将后续学习单片机、PLC、深度学习的笔记全部沉淀在这里。  
2. 我可以借助这个机会将我零散的编程知识（Python、一些小的基础）串联起来。  
3. 我可以找到一个平台去提供我以后的软件项目的下载链接，以及硬件项目的开源链接。

### 我要展示什么？

1. About Me: 我的专业、年级、研究兴趣、个人经历、以及实时更新的简历。
2. Portfolio: 我的项目集，作品集
3. Blogs & Notes: 记录我对于算法的理解，以及把我在项目中学到的破碎的知识点整合成为可视化的，我自己的东西。
4. Contact: 我的邮箱、Github账号，使得如果有机会的话大家可以联系到我。

### 我要用什么工具？

由于我要进行数据存储（博客文章，用户评论）和文件管理（项目下载，大文件上云），我会需要：

1. 后端的框架来处理逻辑
2. 数据库，来存储我的文字和信息
3. 一定的前端来展示我的页面

所以我可以利用我在蓝桥上面学到的一定的Django的知识。相较于Flask，Django可以让我：

1. 免去完全由自己写登陆系统、上传页面、数据库链接的时间，让这个项目不那么复杂和沉重。
2. Django 自带一个很强大的**后台管理系统 (Admin)**和**数据库管理工具 (ORM)**，它可以让我想操作对象一样操作数据库。

作为前端，我不想太过注重，还是要先学好后端。 ~~不然我的担子也太重了点。~~

问过GPT之后给我的推荐是Bootstrap，因为作为 CSS 框架，我可以相对省力的开发前端。

**所以，我的技术栈将会是：**
- **语言：** Python 3
- **后端框架：** Django
- **数据库：** SQLite (Django 自带)
- **前端：** HTML5 + Bootstrap 5 + Django Template

---

### 架构理解

我很认同的一点是，我需要先理解网站是怎么活过来的。Gemini 给我的比方是“控制回路”：

1. **用户 (User)：** 在浏览器中点击项目的链接。
2. **URL路由 (urls.py)：** 就像分拣机，识别到请求是`/download/project-a`，把它丢给对应的处理函数。
3. **视图 (views.py)：** 这是**控制器 (Controller)**。它会去数据库查找项目的路径，并读取文件。
4. **模型 (models.py)：** 我在这里定义项目的样子（名字、上传时间、文件路径）。
5. **模板 (templates)：** 这是**HMI(人机界面)**。后端把数据填进 HTML 坑里，发回给用户。

---

### 环境配置

很多东西，就算已经会了，也是需要常用常新。特此记录下来，以作警示。

#### 1. 虚拟环境

Python 开发最忌讳库的版本冲突。因此我们需要创建虚拟环境。创建虚拟环境的命令行代码如下：

``` Bash
# 1.创建一个项目文件夹
mkdir Project
cd Project

# 2.创建虚拟环境 (名字叫 venv)
python -m venv venv

# 3.激活虚拟环境
# Windows
.\venv\Scripts\activate
# Linux
source venv/bin/activate

# 激活成功后，你的命令行前会出现 (venv) 字样
```

后续安装我们都会在虚拟环境中进行

#### 安装 Django

在激活的虚拟环境中输入：

``` bash
pip install django
```

> **使用任何库之前都要去读一下官方的文档，这一点很重要！**

---

### 总结

今天配置了一些基础的环境，想明白了我做这个网站的方向。以后再做任何的项目前，我都应该像这样想一下。

---

## Day 1: 创建骨架及应用

只要处在 Python 开发环境下，最好保证虚拟环境 `(venv)` 已经打开。

### 使用 Django 创建项目

确保我们在 `Project` 文件夹下，在命令行中输入命令：

``` bash
django-admin startproject Project .
```

> **我们应当注意的是，最后的点 `(.)` 非常重要！** 这表示“在当前目录下创建项目”。

于是我们可以得到如下的目录结构：

``` Text
MyWebsite/
    venv/                   # 虚拟环境文件夹
    manage.py               # 项目的管理脚本
    Project/                # 配置文件夹
        __init__.py
        settings.py         # 配置文件
        urls.py             # 路由文件
        wsgi.py
        asgi.py
```

在成功创建项目后，我们可以测试服务器并到 `http://127.0.0.1:8000/` 去在本地进行测试。 Django 的默认页面是一个小火箭。按 *`CTRL + C`* 可以停止服务器。

---

### 在 Django 中创建应用

Django 的设计理念是：一个 Project 由多个 App 组成，比如一个 App 管博客，一个 App 管用户登录。

让我们以 `app_1` 来举例。

``` Bash
python manage.py startapp app_1
```

在成功创建 App 之后，我们需要在 setings.py 中注册这个 App 来让项目知道 App 的存在

1. 打开 `Project/settings.py` 。
2. 找到 `INSTALLED_APPS` 列表。
3. 在列表的最后添加 `'app_1',` 。

```Python
# Project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... 其他默认Apps ...
    'django.contrib.staticfiles', 

    # 为了日后方便查找，我习惯在这里额外加行空行
    'app_1',     # <-- 注意！一定要加逗号！
]
```

> 在这里，由于我的网站的主要目的是做我个人的项目展示，我的项目名称叫做 `My_Portfolio` ，而我选择创建的第一个 App 被命名为 `'main'` ，用来实现一些相对主要的内容。

---

### 编写我的第一个视图

我们现在要让网站真正显示我们的东西，而不是默认的小火箭。这需要走通 **MVT (Model, View, Template)** 流程中的 **VT (View -> Template)** 。

#### 写视图 (Views - 控制器)

打开 `main/views.py` ，更改里面的内容：

``` Python

from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>你好，这里是我的个人主页！</h1>")
```

#### 配置路由 (URLs - 导航仪)

现在要告诉 Django, 当用户访问首页的时候，去调用 `home` 这个函数。  
打开 `myportfolio/urls.py` ，修改如下：

``` Python
from django.contrib import admin
from django.urls import path, include

from main import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', view.home, name='home'),   # 空字符串表示首页
]
```

#### 测试
在保存所有文件之后运行服务器，进入 `heep://127.0.0.1:8000/` ，你应该能看到白底黑字的“你好，这是我的个人主页！”

---

### 引入 HTML 模板（穿上衣服）

用 `HttpResponse` 写 HTML 字符串太痛苦了。因此，我们要用独立的 HTML 文件。

#### **创建 `Templates` 文件夹：**
    在 `main` 文件夹下，创建一个叫 `templates` 的文件夹。
    在 `templates` 里面，**再**创建一个叫 `main` 的文件夹。  
    *结构：`main/templates/main/`*  
    *(为什么要多套一层 main？这是 Django 的命名空间规范，防止不同 App 的模板重名。)*

#### **创建 HTML 文件：**
    在 `main/templates/main/` 下新建 `home.html`，输入：

    ``` html
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>我的主页</title>
        <!-- 引入 Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        
        <!-- 导航栏 -->
        <nav class="navbar navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="#">自动化工程师的站点</a>
            </div>
        </nav>

        <!-- 主体内容 -->
        <div class="container mt-5">
            <div class="card">
                <div class="card-body">
                    <h1 class="card-title">欢迎！</h1>
                    <p class="card-text">这是我用 Django 搭建的第一个全栈页面。</p>
                    <a href="#" class="btn btn-primary">查看项目</a>
                </div>
            </div>
        </div>

    </body>
    </html>
    ```

#### **修改视图 (Views) 并使用模板：**
    回到 `main/views.py`，修改 `home` 函数：

    ```python
    from django.shortcuts import render

    def home(request):
        # 这里的路径是从 templates 文件夹内部开始算的
        return render(request, 'main/home.html') 
    ```

这时，再刷新浏览器，我们就能够看到一个带有蓝色导航栏和卡片样式的页面了。

---

### 总结
今天，我们跑通了 Django 的 VT 流程，配置好了项目的基本结构，并通过 Bootstrap 引入了外部的 CSS 框架。








