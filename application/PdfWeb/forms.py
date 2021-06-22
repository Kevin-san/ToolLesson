#-*-coding:utf-8-*-
'''
Created on 2020/09/06

@author: xcKev
'''
from django import forms
from captcha.fields import CaptchaField
from PdfWeb import db
from django.forms import fields
from mdeditor.fields import MDTextFormField
gender = (
        ('1', "男"),
        ('0', "女"),
)
blog_categorys = db.get_blog_category_type_info().values_list('CategoryId','CategoryName')
tag_categorys = db.get_blog_tag_category_type_info().values_list('CategoryId','CategoryName')
original_categorys = (
    (0,'原创'),
    (1,'转载')
)

type_categorys = (
    (0,'草稿'),
    (1,'正式')
)

permissions= (
        ('b1c1d8e4f4g1','默认游客'), # 博客 读 课程 读  小说 读 
        ('b1c2d8e4f4g1','博客博主'), # 博客 读写
        ('b4c2d8e4f4g1','课程文人'), # 课程 读写上传
        ('b8c2d8e4f4g1','课程骚客'), # 课程 读写上传下载
        ('b2c2d8e4f4g4','小说捉笔'), # 小说 读写上传
        ('b2c2d8e4f4g8','小说墨客'), # 小说 读写上传下载
        ('b1c1d8e8f4g1','音频知己'), # 音频 上传 下载
        ('b1c1d8e8f8g1','视频光影'), # 视频 上传 下载
        ('b8c8d8e8f8g8','都要大人'), # 所有 除了 hiders
        ('0','幕后黑手'), # + hiders
)
class Searchform(forms.Form):
    """搜索表单"""
    s = forms.CharField(max_length=20)

class CommentForm(forms.Form):
    """博客评论"""
    Content = fields.CharField(label="评论内容",min_length=10,error_messages={"required":"不能为空","invalid":"格式错误","min_length":"评论内容最短10位"})

class ArticleForm(forms.Form):
    """博客内容  form 需要修改优化,views services 同步修改"""
    Id= fields.IntegerField(initial=-1,widget=forms.widgets.HiddenInput)
    AuthorId = fields.IntegerField(initial=-1,widget=forms.widgets.HiddenInput)
    Title = fields.CharField(label="标题",min_length=10,error_messages={"required":"不能为空","invalid":"格式错误","min_length":"标题最短10位"})
    Synopsis = fields.CharField(label="简介",min_length=20,error_messages={"required":"不能为空","invalid":"格式错误","min_length":"简介最短20位"})
    CategoryId = fields.ChoiceField(label="所属分类",choices=blog_categorys,initial=30,widget=forms.widgets.Select)
    TagId = fields.ChoiceField(label="所属标签",choices=tag_categorys,initial=60,widget=forms.widgets.Select)
    Type = fields.ChoiceField(label="草稿正式",choices=type_categorys,initial=0,widget=forms.widgets.Select)
    Original = fields.ChoiceField(label="转载原创",choices=original_categorys,initial=0,widget=forms.widgets.Select)
    Content = MDTextFormField(label="正文内容",min_length=100,error_messages={"required":"不能为空","invalid":"格式错误","min_length":"简介最短100位"})
    
class Tagform(forms.Form):
    """tag搜索表单"""
    t = forms.CharField(max_length=20)

class EditUserForm(forms.ModelForm):
    Id= fields.IntegerField(widget=forms.widgets.HiddenInput)
    Name = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    Sex = forms.ChoiceField(label='性别', choices=gender)
    Logo = forms.ImageField(label='个人头像')
    Detail = forms.CharField(label="个人简介",max_length=1000,widget=forms.TextInput(attrs={'class': 'form-control'}))
    

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')
    
class RegisterForm(forms.Form):

    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    logo = forms.ImageField(label='个人头像')
    detail = forms.CharField(label="个人简介",max_length=1000,widget=forms.TextInput(attrs={'class': 'form-control'}))
    permissions = forms.ChoiceField(label='角色',choices=permissions)
    captcha = CaptchaField(label='验证码')