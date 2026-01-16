from django import forms

class ContactForm(forms.Form):
    # 定义表单字段，类似 Model 但不需要存数据库
    name = forms.CharField(
        max_length=50, 
        label='您的称呼',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓名'})
    )
    email = forms.EmailField(
        label='您的邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'})
    )
    subject = forms.CharField(
        max_length=100, 
        label='邮件主题',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='正文内容', 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )