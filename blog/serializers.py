from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Comment

# 定义 User 的序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# 定义 Comment 的序列化器
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body', 'created_at']

# 定义 Post 的序列化器
class PostSerializer(serializers.ModelSerializer):
    # 嵌套显示：不要只返回 author_id=1，而是返回 {id:1, username:"admin"}
    author = UserSerializer(read_only=True)
    
    # 嵌套显示评论：把这篇文章的所有评论也带出来 (可选，如果评论太多建议分开查)
    # comments = CommentSerializer(many=True, read_only=True)
    
    # 或者只返回评论数量
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'created_at', 'comment_count']
        # 注意：列表页通常不返回 content (正文)，太大了。详情页才返回。

    def get_comment_count(self, obj):
        return obj.comments.count()

# 详情页专用的 Serializer (包含正文)
class PostDetailSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['content']