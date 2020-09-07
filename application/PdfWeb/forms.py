#-*-coding:utf-8-*-
'''
Created on 2020/09/06

@author: xcKev
'''
from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')
    
class RegisterForm(forms.Form):
    gender = (
        ('1', "男"),
        ('0', "女"),
    )
    permissions= [
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
    ]
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    permissions = forms.ChoiceField(label='角色',choices=permissions)
    captcha = CaptchaField(label='验证码')