from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 只让用户填写这三项, post 和 created_at 自动处理
        fields = ('name', 'email', 'body')

        # 给控件加 Bootstrap 样式
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '你的昵称'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '你的邮箱（不会公开）'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '写下你的想法...'}),
        }