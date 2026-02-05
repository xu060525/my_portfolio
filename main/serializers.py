from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # 定义想要在 API 中暴露的字段
        fields = '__all__'