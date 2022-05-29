#-*- encoding:UTF-8 -*-
'''
Created on 2020/09/06

@author: xcKev
'''
from django import forms
from captcha.fields import CaptchaField
from PdfWeb import db
from django.forms import fields
from mdeditor.fields import MDTextFormField
from django.core import validators
gender = (
        ('1', "男"),
        ('0', "女"),
)
blog_categorys = list(db.get_blog_category_type_info().values_list('CategoryId','CategoryName'))
tag_categorys = list(db.get_blog_tag_category_type_info().values_list('CategoryId','CategoryName'))
novel_categorys = list(db.get_novel_category_type_info().values_list('CategoryId','CategoryName'))
learn_categorys = list(db.get_learn_category_type_info().values_list('CategoryId','CategoryName'))
image_categorys = list(db.get_image_category_type_info().values_list('CategoryId','CategoryName'))
audio_categorys = list(db.get_audio_category_type_info().values_list('CategoryId','CategoryName'))
video_categorys = list(db.get_video_category_type_info().values_list('CategoryId','CategoryName'))
vhider_categorys = list(db.get_vhider_category_type_info().values_list('CategoryId','CategoryName'))
all_categorys=blog_categorys+tag_categorys+novel_categorys+learn_categorys+image_categorys+audio_categorys+video_categorys+vhider_categorys
all_categorys_map=dict(all_categorys)
original_categorys = (
    (1,'原创'),
    (0,'转载')
)

type_categorys = (
    (0,'草稿'),
    (1,'正式')
)
preffix_map={"image":"jpg","audio":"mp3","video":"mp4","learn":"pdf","novel":"txt"}
permissions= (
        ('b1c1d1e1f1g1i1','网站游客'), # read and novel/blog/learn/image/video/audio
        ('b1c1d1e1f1g1h1i1','网站间客'), # read and novel/blog/learn/image/video/audio/vhider
        ('b1c1d1e1f1g1i2','图片下载'), # read and image : export 
        ('b1c1d1e1f2g1i1','视频下载'), # read and video : export 
        ('b1c1d1e2f1g1i1','音频下载'), # read and audio : export 
        ('b1c1d1e1f1g1i8','图片上传'), # read and image : import 
        ('b1c1d1e1f8g1i1','视频上传'), # read and video : import 
        ('b1c1d1e8f1g1i1','音频上传'), # read and image : import 
        ('b1c1d1e1f1g4i1','小说作者'), # read and novel : write
        ('b4c1d1e1f1g1i1','教程作者'), # read and learn : write
        ('b1c1d1e1f1g8i1','小说编辑'), # read and novel : import
        ('b8c1d1e1f1g1i1','教程编辑'), # read and learn : import
        ('b1c1d1e4f4g1i4','媒体下载'), # read and image/video/audio : export
        ('b1c1d1e8f8g1i8','媒体上传'), # read and image/video/audio : export
        ('b4c1d1e1f1g4i1','文理作者'), # read and novel/blog/learn : write
        ('b8c1d1e1f1g8i1','文理编辑'), # read and novel/blog/learn : import
        ('b2c2d2e2f2g2i2','综合下载'), # read and novel/blog/learn/image/video/audio : export
        ('b2c2d2e2f2g2h2i2','综艺下载'), # read and novel/blog/learn/image/video/audio/vhider : export
        ('b8c8d8e8f8g8i8','综合上传'), # read and novel/blog/learn/image/video/audio : import
        ('b9c9d9e9f9g9h9i9','管理员'), # + hiders
)
class Searchform(forms.Form):
    """搜索表单"""
    s = forms.CharField(max_length=20)

class CommentForm(forms.Form):
    """博客评论"""
    Content = fields.CharField(label="评论内容",min_length=10,error_messages={"required":"不能为空","invalid":"格式错误","min_length":"评论内容最短10位"})

class TxtUploadForm(forms.Form):
    """文本上传页面"""
    title=forms.CharField(label="标题",max_length=100,error_messages={"required":"不能为空","invalid":"格式错误"})
    CategoryId = fields.ChoiceField(label="所属分类",choices=novel_categorys,initial=101,widget=forms.widgets.Select)
    description=forms.CharField(label="简介",max_length=300,error_messages={"required":"不能为空","invalid":"格式错误"})
    author=forms.CharField(label="作者",max_length=100,error_messages={"required":"不能为空","invalid":"格式错误"})
    file=forms.FileField(label="小说",validators=[validators.FileExtensionValidator(['txt'],message='小说必须是txt文件')])
    action="/novel/book/upload"

class PdfUploadForm(forms.Form):
    """Pdf上传页面"""
    title=forms.CharField(label="标题",max_length=100,error_messages={"required":"不能为空","invalid":"格式错误"})
    CategoryId = fields.ChoiceField(label="所属分类",choices=learn_categorys,initial=11,widget=forms.widgets.Select)
    description=forms.CharField(label="简介",max_length=300,error_messages={"required":"不能为空","invalid":"格式错误"})
    author=forms.CharField(label="作者",max_length=100,error_messages={"required":"不能为空","invalid":"格式错误"})
    chapterPages=forms.Textarea(label="章节页号",error_messages={"required":"不能为空","invalid":"格式错误"})
    file=forms.FileField(label="教程",validators=[validators.FileExtensionValidator(['pdf'],message='教程必须是pdf文件')])
    action="/learn/book/upload"

class Mp3UploadForm(forms.Form):
    """音频上传页面"""
    title=forms.CharField(label="标题",max_length=100,error_messages={"required":"不能为空","invalid":"格式错误"})
    CategoryId = fields.ChoiceField(label="所属分类",choices=audio_categorys,initial=301,widget=forms.widgets.Select)
    description=forms.CharField(label="简介",max_length=300,error_messages={"required":"不能为空","invalid":"格式错误"})
    file=forms.FileField(label="音频",validators=[validators.FileExtensionValidator(['mp3'],message='音频必须是mp3文件')])
    action="/audio/media/upload"

class JpgUploadForm(forms.Form):
    """图片上传界面"""
    title=forms.CharField(label="标题",max_length=100,error_messages={"required":"不能为空","invalid":"格式错误"})
    CategoryId = fields.ChoiceField(label="所属分类",choices=image_categorys,initial=215,widget=forms.widgets.Select)
    description=forms.CharField(label="简介",max_length=300,error_messages={"required":"不能为空","invalid":"格式错误"})
    file=forms.ImageField(label="图片",validators=[validators.FileExtensionValidator(['jpg'],message='图片必须是jpg文件')])
    action="/image/media/upload"

class Mp4UploadForm(forms.Form):
    """视频上传界面"""
    title=forms.CharField(label="标题",max_length=100,error_messages={"required":"不能为空","invalid":"格式错误"})
    CategoryId = fields.ChoiceField(label="所属分类",choices=video_categorys,initial=5001,widget=forms.widgets.Select)
    description=forms.CharField(label="简介",max_length=300,error_messages={"required":"不能为空","invalid":"格式错误"})
    file=forms.FileField(label="视频",validators=[validators.FileExtensionValidator(['mp4'],message='视频必须是mp4文件')])
    action="/video/media/upload"

class BookForm(forms.Form):
    Id= fields.IntegerField(initial=0,widget=forms.widgets.HiddenInput)
    BookName = fields.CharField(label="名字",error_messages={"required":"书名不能为空"})
    Description = fields.CharField(label="简介",widget=forms.Textarea,error_messages={"required":"简介不能为空"})
    Author = fields.CharField(label="作者",error_messages={"required":"作者不能为空"})
    ImageContent=forms.ImageField(label='图片',error_messages={"required":"图片不能为空"})

class SectionForm(forms.Form):
    Id= fields.IntegerField(initial=0,widget=forms.widgets.HiddenInput)
    BookId= fields.IntegerField(initial=0,widget=forms.widgets.HiddenInput)
    OrderNo= fields.IntegerField(initial=0,widget=forms.widgets.HiddenInput)
    SectionNo= fields.IntegerField(initial=0,widget=forms.widgets.HiddenInput)
    ChapterName = fields.CharField(label="章节名",error_messages={"required":"不能为空"})
    Content = MDTextFormField(label="内容",error_messages={"required":"不能为空"})

class NovelForm(BookForm):
    CategoryId = fields.ChoiceField(label="所属分类",choices=novel_categorys,initial=101,widget=forms.widgets.Select)

class LearnForm(BookForm):
    CategoryId = fields.ChoiceField(label="所属分类",choices=learn_categorys,initial=11,widget=forms.widgets.Select)

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

class EditUserForm(forms.Form):
    Id= fields.IntegerField(widget=forms.widgets.HiddenInput)
    Name = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    Sex = forms.ChoiceField(label='性别', choices=gender)
    Logo = forms.ImageField(label='个人头像',required=False)
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