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

class UserFunction(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='Id')
    GroupKey = models.CharField(max_length=30, unique=True,verbose_name='用户组')
    RoleId = models.IntegerField(verbose_name='权限Id')
    FunctionStr = models.CharField(max_length=256,verbose_name='功能模块')
    DeleteFlag=models.BooleanField(default=1,verbose_name='删除状态')
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='UserFunction'
        verbose_name = "用户功能"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.FunctionStr

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

class Category(models.Model):
    CategoryId=models.IntegerField(primary_key=True,verbose_name='Id')
    CategoryName=models.CharField(max_length=200,verbose_name='类别名')
    CategoryValue1=models.CharField(max_length=200,verbose_name='类别值1')
    CategoryValue2=models.CharField(max_length=200,verbose_name='类别值2')
    CategoryValue3=models.CharField(max_length=200,verbose_name='类别值3')
    CategoryFather=models.IntegerField(verbose_name='父类Id')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='Category'
        verbose_name='分类表'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.CategoryName

class CommonSubFuncs(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='功能Id')
    FunctionName=models.CharField(max_length=100,verbose_name='功能名')
    FunctionHref=models.CharField(max_length=100,verbose_name='功能链接')
    FunctionDesc=models.CharField(max_length=500,verbose_name='功能细节')
    CommonMainType_Id=models.IntegerField(verbose_name='主功能类别Id')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='CommonSubFuncs'
        verbose_name='功能信息表'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.FunctionName
    
class UnitDictionary(models.Model):
    Id=models.IntegerField(primary_key=True,verbose_name='Id')
    ConversionType=models.CharField(max_length=100,verbose_name='换算种类')
    UnitFromKey=models.CharField(max_length=100,verbose_name='因单位')
    UnitToKey=models.CharField(max_length=500,verbose_name='果单位')
    UnitValue=models.IntegerField(verbose_name='单位值')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='UnitDictionary'
        verbose_name='换算信息表'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.UnitValue