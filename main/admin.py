from django.contrib import admin
from .models import Project, ProjectVersion, Tag

# 定义一个内联块
class VersionInline(admin.TabularInline):
    model = ProjectVersion
    extra = 1   # 默认显示一个空的输入框
    classes = ('collapse',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'created_at', 'get_version_count')

    filter_horizontal = ('tags', )

    search_fields = ('title', 'description')

    list_filter = ('created_at', )

    ordering = ('-created_at', )
    # 加入内联块
    inlines = [VersionInline]

# --- 自定义显示列的方法 ---
    
    # 截取描述的前 30 个字，避免列表太长
    @admin.display(description='描述预览')
    def short_description(self, obj):
        return obj.description[:30] + '...' if obj.description else '-'

    # 统计该项目有多少个版本
    @admin.display(description='版本数')
    def get_version_count(self, obj):
        return obj.versions.count()

# 单独管理版本
@admin.register(ProjectVersion)
class ProjectVersionAdmin(admin.ModelAdmin):
    list_display = ('project', 'version_name', 'created_at')

    list_filter = ('project', 'created_at')

    # 输入项目名字，也能搜出对应的版本。写法是：外键字段名__关联字段名
    search_fields = ('version_name', 'project__title')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name', )}  # 自动填充 slug