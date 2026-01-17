from django.db import models

models.DateTimeField(null=True, blank=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="标签")
    slug = models.SlugField(unique=True, verbose_name="标签别名 (URL用) ")
    # 标签颜色
    color = models.CharField(max_length=20, default='primary', verbose_name="Bootstrap颜色", help_text="可选：primary, secondary, success, danger, warning, info, dark")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "项目标签"
        verbose_name_plural = "标签管理"



class Project(models.Model):
    # CharField 用于短文本，如标题
    title = models.CharField(max_length=100, verbose_name="项目名称")

    # TextField 用于长文本，如项目介绍
    description = models.TextField(verbose_name="项目描述")

    # ImageField 用于图片，需要安装 pillow 库
    # upload_to 指定图片上传到哪个文件夹
    image = models.ImageField(upload_to='project_images/', verbose_name="项目封面")

    # URLField 用于存链接
    github_link = models.URLField(blank=True, verbose_name="GitHub仓库")
    
    # 自动记录创建时间
    created_at = models.DateTimeField(auto_now_add=True)

    # 标签
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="项目标签", related_name="projects")

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目管理"  # 这是一个 Django 的历史遗留梗，复数形式
        ordering = ['-created_at']       # 让最新的项目排在最前面

    def __str__(self):
        return self.title   # 这样在后台就不会显示 "Project object (1)" 而是项目名
    
class ProjectVersion(models.Model):
    # ForeignKey 是关键，它指向父模型 Project
    # related_name='versions' 让我们以后可以用 project.versions.all() 查出所有版本
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='versions', verbose_name="所属项目")

    version_name = models.CharField(max_length=50, verbose_name="版本号", help_text="例如: v1.0, v2.0 beta")
    file = models.FileField(upload_to='porject_files/', verbose_name="项目附件")
    release_note = models.TextField(verbose_name="更新日志/版本说明", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    class Meta:
        ordering = ['-created_at'] # 默认按时间倒序排列（最新的在最上面）
        verbose_name = "项目版本"
        verbose_name_plural = "版本管理"

    def __str__(self):
        return f"{self.project.title} - {self.version_name}"

