from django.db import models

models.DateTimeField(null=True, blank=True)

class Project(models.Model):
    # CharField 用于短文本，如标题
    title = models.CharField(max_length=100, verbose_name="项目名称")

    # TextField 用于长文本，如项目介绍
    description = models.TextField(verbose_name="项目描述")

    # ImageField 用于图片，需要安装 pillow 库
    # upload_to 指定图片上传到哪个文件夹
    image = models.ImageField(upload_to='project_images/', verbose_name="项目封面")
    file = models.FileField(upload_to='project_files/', blank=True, null=True, verbose_name="项目附件")

    # URLField 用于存链接
    github_link = models.URLField(blank=True, verbose_name="GitHub链接")
    
    # 自动记录创建时间
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title   # 这样在后台就不会显示 "Project object (1)" 而是项目名
    
    class Meta:
        verbose_name = "个人项目"
        verbose_name_plural = "个人项目管理"

    
