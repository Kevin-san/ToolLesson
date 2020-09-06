#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from django.db import models

class User(models.Model):
    gender = (
        ('1', "1"),
        ('0', "0"),
    )
    Id=models.IntegerField(primary_key=True,verbose_name='Id')
    Name = models.CharField(max_length=128, unique=True,verbose_name='用户名')
    Password = models.CharField(max_length=256,verbose_name='用户密码')
    Email = models.EmailField(unique=True,verbose_name='用户邮箱')
    Sex = models.CharField(max_length=1, choices=gender, default='1',verbose_name='用户性别')
    Permissions = models.CharField(max_length=128,verbose_name='角色')
    DeleteFlag=models.BooleanField(default=1,verbose_name='删除状态')
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='User'
        verbose_name = "用户"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Name

class UserConfirmString(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='Id')
    code = models.CharField(max_length=256)
    User_Id = models.IntegerField(verbose_name='用户Id')
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ":   " + self.code
    class Meta:
        db_table='UserConfirmString'
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

class BookLessonType(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='课程类别Id')
    CommonType=models.CharField(max_length=100,verbose_name='类别')
    CommonValue=models.CharField(max_length=100,verbose_name='链接')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='BookLessonType'
        verbose_name='书本课程类'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.CommonType

class BookLesson(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='书课Id')
    BookName=models.CharField(max_length=100,verbose_name='书名')
    LessonName=models.CharField(max_length=100,verbose_name='课程名')
    LessonHref=models.CharField(max_length=100,verbose_name='链接')
    BookLessonType_Id=models.IntegerField(verbose_name='课程类别Id')
    Description=models.CharField(max_length=100,verbose_name='大略介绍')
    ImageContent_Id=models.CharField(max_length=100,verbose_name='图片Id')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='BookLesson'
        verbose_name='书本课程'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.Description

class Chapter(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='章节Id')
    BookLesson_Id=models.IntegerField(verbose_name='书本课程Id')
    ChapterNo=models.IntegerField(verbose_name='章节号')
    ChapterName=models.CharField(max_length=100,verbose_name='章节名')
    Href=models.CharField(max_length=100,verbose_name='章节链接')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='Chapter'
        verbose_name='章节'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.ChapterName

class Content(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='段落Id')
    Chapter_Id=models.IntegerField(verbose_name='章节Id')
    ElementTag=models.CharField(max_length=100,verbose_name='段落类')
    OrderIndex=models.IntegerField(verbose_name='段落号')
    AttributeMap=models.CharField(max_length=1000,verbose_name='属性对应')
    Text=models.CharField(max_length=10000,verbose_name='段落内容')
    InnerHtmlText=models.CharField(max_length=10000,verbose_name='段落特别内容')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    
    class Meta:
        db_table='Content'
        verbose_name='段落'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.Text

class ImageContent(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='图片Id')
    Directory=models.CharField(max_length=100,verbose_name='目录')
    ImageName=models.CharField(max_length=100,verbose_name='图片名称')
    Width=models.IntegerField(verbose_name='宽度')
    Height=models.IntegerField(verbose_name='高度')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='ImageContent'
        verbose_name='图片信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Text

class CommonRules(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='Id')
    TypeKey=models.CharField(max_length=100,verbose_name='类型键')
    TypeVal=models.CharField(max_length=100,verbose_name='类型值')
    Rules=models.CharField(max_length=100,verbose_name='规则')
    RulesDescription=models.CharField(max_length=1000,verbose_name='规则细节')
    RulesText=models.CharField(max_length=1000,verbose_name='规则内容')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='CommonRules'
        verbose_name='常用规则'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.RulesText