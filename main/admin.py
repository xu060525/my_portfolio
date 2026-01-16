from django.contrib import admin
from .models import Project, ProjectVersion

# 定义一个内联块
class VersionInline(admin.TabularInline):
    model = ProjectVersion
    extra = 1   # 默认显示一个空的输入框

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    # 加入内联块
    inlines = [VersionInline]

# 单独管理版本
@admin.register(ProjectVersion)
class ProjectVersionAdmin(admin.ModelAdmin):
    list_display = ('project', 'version_name', 'created_at')