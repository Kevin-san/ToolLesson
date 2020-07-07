#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from django.db import models
from tools import common_tools

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
        db_table='LessonImage'
        verbose_name='图片信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Text

class MenuInfo(models.Model):
    MenuType=models.CharField(max_length=100,verbose_name='类别')
    Href=models.CharField(max_length=100,verbose_name='链接')
    Text=models.CharField(max_length=100,verbose_name='内容')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateTimeField(verbose_name="上传时间")
    class Meta:
        db_table='LessonMenu'
        verbose_name='课程目录'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Text

class LessonMenuIndexInfo(models.Model):
    Type=models.CharField(max_length=100,verbose_name='类别')
    Href=models.CharField(max_length=100,verbose_name='链接')
    Alt=models.CharField(max_length=100,verbose_name='别名')
    Title=models.CharField(max_length=100,verbose_name='标题')
    Text=models.CharField(max_length=400,verbose_name='内容')
    ImgSrc=models.CharField(max_length=100,verbose_name='图片位置')
    ImgWidth=models.IntegerField(verbose_name='图片宽度')
    ImgHeight=models.IntegerField(verbose_name='图片高度')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateTimeField(verbose_name="上传时间")
    class Meta:
        db_table='LessonMenuIndex'
        verbose_name='课程子目录'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Text
    
class DetailsInfo(models.Model):
    ParentKey=models.CharField(max_length=100,verbose_name='链接键')
    Type=models.CharField(max_length=100,verbose_name='Tag类别')
    OrderIndex=models.IntegerField(verbose_name='序号')
    AttributeMap=models.CharField(max_length=1000,verbose_name='属性值')
    ClassVal=models.CharField(max_length=500,verbose_name='Class值')
    IdVal=models.CharField(max_length=100,verbose_name='Id值')
    Text=models.CharField(max_length=10000,verbose_name='内容')
    ParentFlag=models.BooleanField(default=False,blank=False,verbose_name='父状态')
    DeleteFlag=models.BooleanField(default=False,blank=False,verbose_name='删除状态')
    submission_user=models.CharField(max_length=30,verbose_name="上传用户")
    submission_date=models.DateTimeField(verbose_name="上传时间")
    class Meta:
        ordering=['OrderIndex']
        db_table='LessonDetails'
        verbose_name='细节信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        tag = self.Type
        t_class_str = F" class='{self.ClassVal}'"
        t_id_str=F" id='{self.IdVal}'"
        class_str=common_tools.get_spec_var(self.ClassVal, "", t_class_str)
        id_str=common_tools.get_spec_var(self.IdVal,"",t_id_str)
        class_id=F"{class_str}{id_str}"
        detail_text = common_tools.get_spec_var(self.Text,"",self.Text)
        if tag in ['hr','br']:
            return F"<{tag}>"
        if tag == 'img':
            img_info = ImageInfo.objects.filter(ImgKey=self.Text)
            return F'<{tag} src="{img_info.Src}" width="{img_info.Width}" height="{img_info.Height}" alt="{img_info.Alt}"{class_id}>'
        return F"<{tag}{class_id}>{detail_text}</{tag}>"
