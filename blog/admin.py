from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    # 自动根据标题填充 slug，方便偷懒
    prepopulated_fields = {'slug': ('title',)}