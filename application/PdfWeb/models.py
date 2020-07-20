#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from django.db import models

class BookLessonTypeInfo(models.Model):
    Id=models.IntegerField(verbose_name='课程类别Id')
    CommonType=models.CharField(max_length=100,verbose_name='类别')
    CommonValue=models.CharField(max_length=100,verbose_name='链接')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateTimeField(verbose_name="上传时间")
    class Meta:
        db_table='BookLessonType'
        verbose_name='书本课程类'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.CommonType

class BookLessonInfo(models.Model):
    Id=models.IntegerField(verbose_name='书课Id')
    BookName=models.CharField(max_length=100,verbose_name='书名')
    LessonName=models.CharField(max_length=100,verbose_name='课程名')
    LessonHref=models.CharField(max_length=100,verbose_name='链接')
    LessonTypeId=models.IntegerField(verbose_name='课程类别Id')
    Description=models.CharField(max_length=100,verbose_name='大略介绍')
    ImageId=models.CharField(max_length=100,verbose_name='图片Id')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateTimeField(verbose_name="上传时间")
    class Meta:
        db_table='BookLesson'
        verbose_name='书本课程'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.Description

class ChapterInfo(models.Model):
    Id=models.IntegerField(verbose_name='章节Id')
    BookLessonId=models.IntegerField(verbose_name='书本课程Id')
    ChapterNo=models.IntegerField(verbose_name='章节号')
    ChapertName=models.CharField(max_length=100,verbose_name='章节名')
    Href=models.CharField(max_length=100,verbose_name='章节链接')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateTimeField(verbose_name="上传时间")
    class Meta:
        db_table='Chapter'
        verbose_name='章节'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.ChapertName
class ContentInfo(models.Model):
    Id=models.IntegerField(verbose_name='段落Id')
    ChapterId=models.IntegerField(verbose_name='章节Id')
    ElementTag=models.CharField(max_length=100,verbose_name='段落类')
    OrderIndex=models.IntegerField(verbose_name='段落号')
    AttributeMap=models.CharField(max_length=1000,verbose_name='属性对应')
    Text=models.CharField(max_length=10000,verbose_name='段落内容')
    InnerHtmlText=models.CharField(max_length=10000,verbose_name='段落特别内容')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateTimeField(verbose_name="上传时间")
    class Meta:
        db_table='Content'
        verbose_name='段落'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.Text
class ImageContentInfo(models.Model):
    Id=models.IntegerField(verbose_name='图片Id')
    Directory=models.CharField(max_length=100,verbose_name='目录')
    ImageName=models.CharField(max_length=100,verbose_name='图片名称')
    Width=models.IntegerField(verbose_name='宽度')
    Height=models.IntegerField(verbose_name='高度')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateTimeField(verbose_name="上传时间")
    class Meta:
        db_table='ImageContent'
        verbose_name='图片信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Text

class CommonRulesInfo(models.Model):
    Id=models.IntegerField(verbose_name='Id')
    TypeKey=models.CharField(max_length=100,verbose_name='类型键')
    TypeValue=models.CharField(max_length=100,verbose_name='类型值')
    Rules=models.CharField(max_length=100,verbose_name='规则')
    RulesDescription=models.CharField(max_length=1000,verbose_name='规则细节')
    RulesText=models.CharField(max_length=1000,verbose_name='规则内容')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateTimeField(verbose_name="上传时间")
    class Meta:
        db_table='CommonRules'
        verbose_name='常用规则'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.RulesText