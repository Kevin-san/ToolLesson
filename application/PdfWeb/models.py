#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from django.db import models
import time

def user_directory_path(instance,filename):
    childdir= time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
    return 'img/article/{0}/{1}'.format(childdir,filename)

def book_directory_path(instance,filename):
    childdir= time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
    return 'img/book/{0}/{1}'.format(childdir,filename)

def avdeo_directory_path(instance,filename):
    childdir= time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
    return 'img/avdeo/{0}/{1}'.format(childdir,filename)

class Media(models.Model):
    Id=models.AutoField(primary_key=True,verbose_name='Id')
    MediaName = models.CharField(max_length=100, unique=True,verbose_name='音视频名')
    ParentDir = models.CharField(max_length=100,verbose_name='父目录')
    Content = models.CharField(max_length=3000,verbose_name='内容')
    Authors = models.CharField(max_length=300,default='',verbose_name='作者')
    ImageContent = models.ImageField(upload_to=avdeo_directory_path,max_length=100,default='',verbose_name='图片',null=True,blank=True)
    CategoryId= models.IntegerField(verbose_name='分类Id')
    TotalTime = models.IntegerField(verbose_name='总时长')
    TotalSize = models.IntegerField(verbose_name='总大小')
    UpdateTime=models.DateTimeField(auto_now_add=True,verbose_name="更新时间")
    UpdateUser=models.CharField(max_length=100,verbose_name='更新者')
    DeleteFlag=models.BooleanField(default=0,verbose_name='删除状态')
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='Media'
        verbose_name = "音视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.AvName

class MediaSection(models.Model):
    Id=models.AutoField(primary_key=True,verbose_name='Id')
    MediaId = models.IntegerField(verbose_name='MediaId')
    OrderNo = models.IntegerField(default=0,verbose_name='章号')
    SectionNo = models.IntegerField(default=0,verbose_name='节号')
    Preffix = models.CharField(max_length=10,verbose_name='后缀')
    Time = models.IntegerField(verbose_name='时长')
    Size = models.BigIntegerField(verbose_name='大小')
    UpdateTime=models.DateTimeField(auto_now_add=True,verbose_name="更新时间")
    UpdateUser=models.CharField(max_length=100,verbose_name='更新者')
    DeleteFlag=models.BooleanField(default=0,verbose_name='删除状态')
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='MediaSection'
        verbose_name = "音视频集"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.OrderNo+"."+self.Preffix

class Book(models.Model):
    Id=models.AutoField(primary_key=True,verbose_name='书课Id')
    BookName=models.CharField(max_length=100,verbose_name='书名')
    Description=models.CharField(max_length=100,verbose_name='大略介绍')
    Author=models.CharField(max_length=100,verbose_name='作者')
    ImageContent=models.ImageField(upload_to=book_directory_path,max_length=300,verbose_name='图片',null=True,blank=True)
    CategoryId= models.IntegerField(verbose_name='分类Id')
    MaxSectionId= models.IntegerField(verbose_name='最新Id')
    MaxSectionName=models.CharField(max_length=300,verbose_name='最新标题')
    UpdateTime=models.DateTimeField(auto_now_add=True,verbose_name="更新时间")
    UpdateUser=models.CharField(default='alvin',max_length=100,verbose_name='更新者')
    DeleteFlag=models.BooleanField(default=0,verbose_name='删除状态')
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='Book'
        verbose_name='书'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.Description

class Section(models.Model):
    Id=models.AutoField(primary_key=True,verbose_name='章节Id')
    BookId=models.IntegerField(verbose_name='书本Id')
    OrderNo=models.IntegerField(verbose_name='章号')
    SectionNo=models.IntegerField(verbose_name='节号')
    ChapterName=models.CharField(max_length=100,verbose_name='章节名')
    Content=models.TextField(verbose_name='内容')
    UpdateTime=models.DateTimeField(auto_now_add=True,verbose_name="更新时间")
    UpdateUser=models.CharField(default='alvin',max_length=100,verbose_name='更新者')
    DeleteFlag=models.BooleanField(default=0,verbose_name='删除状态')
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    class Meta:
        db_table='Section'
        verbose_name='章节'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.ChapterName

class AcImage(models.Model):
    '''相册'''
    image_title = models.CharField(max_length=20, verbose_name=u'图片标题', default='')
    image_detail = models.CharField(max_length=200, verbose_name=u'图片简介', default='')
    image_path = models.ImageField(upload_to="upload/%Y/%m", default="upload/default.jpg", max_length=100, verbose_name=u"图片")

    class Meta:
        db_table='AcImage'
        verbose_name = u'网站相册'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.image_title

class User(models.Model):
    gender = (
        ('1', "1"),
        ('0', "0"),
    )
    Id=models.AutoField(primary_key=True,verbose_name='Id')
    Name = models.CharField(max_length=128, unique=True,verbose_name='用户名')
    Password = models.CharField(max_length=256,verbose_name='用户密码')
    Email = models.EmailField(unique=True,verbose_name='用户邮箱')
    Sex = models.CharField(max_length=1, choices=gender, default='1',verbose_name='用户性别')
    Logo = models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    Detail= models.CharField(max_length=1000,verbose_name='个人简介')
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
    Id=models.AutoField(primary_key=True,verbose_name='Id')
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
    Id=models.AutoField(primary_key=True,verbose_name='Id')
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
    Id=models.AutoField(primary_key=True,verbose_name='书课Id')
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
    Id=models.AutoField(primary_key=True,verbose_name='章节Id')
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
    Id=models.AutoField(primary_key=True,verbose_name='段落Id')
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
    Id=models.AutoField(primary_key=True,verbose_name='图片Id')
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
    Id=models.AutoField(primary_key=True,verbose_name='Id')
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
    CategoryId=models.AutoField(primary_key=True,verbose_name='CategoryId')
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
    Id=models.AutoField(primary_key=True,verbose_name='功能Id')
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
    Id=models.AutoField(primary_key=True,verbose_name='Id')
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

class Comment(models.Model):
    """博客评论"""
    Id=models.AutoField(primary_key=True,verbose_name='Id')
    ArticleId=models.IntegerField(verbose_name='ArticleId')
    Content= models.CharField(max_length=3000,verbose_name=u'评论内容', default='')
    AuthorId = models.IntegerField(verbose_name=u'作者Id')
    AuthorName = models.CharField(max_length=200, verbose_name=u'作者昵称')
    DeleteFlag=models.BooleanField(default=1,verbose_name='删除状态')
    CreateTime= models.DateTimeField(verbose_name=u'创建时间',  auto_now_add=True)
    UpdateTime= models.DateTimeField(verbose_name=u'更新时间',  auto_now=True)
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
    
    class Meta:
        db_table='Comment'
        verbose_name=u'评论表'
        verbose_name_plural = verbose_name

class Article(models.Model):
    """博客文章"""
    Id=models.AutoField(primary_key=True,verbose_name='Id')
    Title = models.CharField(max_length=50, verbose_name=u'日志标题', default='')
    Synopsis = models.CharField(max_length=1000,verbose_name=u'日志简介', default='')
    AuthorId = models.IntegerField(verbose_name=u'作者Id')
    AuthorName = models.CharField(max_length=200, verbose_name=u'作者昵称')
    CategoryId = models.IntegerField(verbose_name=u'所属分类')
    CategoryName = models.CharField(max_length=200, verbose_name=u'分类名称')
    TagId = models.IntegerField(verbose_name=u'所属标签')
    TagName = models.CharField(max_length=200,verbose_name=u'日志标签',default='')
    Content = models.CharField(max_length=10000,verbose_name=u'日志正文')
    Type = models.IntegerField(default=0, verbose_name=u"文章类别")
    Original = models.IntegerField(default=1, verbose_name=u"是否原创")
    Click = models.PositiveIntegerField(verbose_name=u'文章点击量', default=0)
    Up = models.IntegerField(default=0, verbose_name=u"文章置顶")
    Support= models.IntegerField(default=0, verbose_name=u"文章推荐")
    CreateTime= models.DateTimeField(verbose_name=u'创建时间',  auto_now_add=True)
    UpdateTime= models.DateTimeField(verbose_name=u'更新时间',  auto_now=True)
    DeleteFlag=models.BooleanField(default=0,verbose_name='删除状态')
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")
        
    class Meta:
        db_table='Article'
        verbose_name=u'文章表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Title
    def increase_article_click(self):
        """文章点击量"""
        self.Click += 1
        self.save(update_fields=['Click'])
        
class SiteInfo(models.Model):
    """站点信息"""
    Id=models.IntegerField(primary_key=True,verbose_name='Id')
    Name = models.CharField(max_length=20, verbose_name=u'站点名称', default='')
    Detail = models.CharField(max_length=100, verbose_name=u'站点介绍', default='')
    User = models.ForeignKey(User,verbose_name=u'管理员',on_delete=models.CASCADE)
    Logo = models.ImageField(upload_to="site/", default="site/default.png", max_length=100, verbose_name=u"站点logo")
    TopImage = models.ImageField(upload_to="site/", default="site/topbg.jpg", max_length=100, verbose_name=u"顶部大图")
    Powered = models.CharField(max_length=100, verbose_name=u'Powered By', default='')
    Links = models.CharField(max_length=100, verbose_name=u'links', default='')
    ContactEmail = models.CharField(max_length=100,verbose_name=u'contact me Email:', default='')
    ContactQQ = models.CharField(max_length=100,verbose_name=u'contact me QQ:', default='')
    DeleteFlag=models.BooleanField(default=1,verbose_name='删除状态')
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")

    class Meta:
        db_table='SiteInfo'
        verbose_name = u'网站信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Name
    
class SpiderSource(models.Model):
    """爬虫源"""
    Id=models.IntegerField(primary_key=True,verbose_name='Id')
    Name = models.CharField(max_length=50, verbose_name=u'名字', default='')
    Section = models.CharField(max_length=50, verbose_name=u'分类', default='')
    Url = models.CharField(max_length=3000,verbose_name=u'网址',default='')
    Attr = models.CharField(max_length=3000,verbose_name=u'属性',default='')
    DeleteFlag=models.IntegerField(default=1,verbose_name='删除状态')
    CreateTime= models.DateTimeField(verbose_name=u'创建时间',  auto_now_add=True)
    UpdateTime= models.DateTimeField(verbose_name=u'更新时间',  auto_now=True)
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")

    class Meta:
        db_table='SpiderSource'
        verbose_name = u'爬虫源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Section
    
class SpiderItem(models.Model):
    """爬虫个体"""
    Id=models.IntegerField(primary_key=True,verbose_name='Id')
    SourceId=models.IntegerField(verbose_name='SourceId')
    Url = models.CharField(max_length=10000,verbose_name=u'网址',default='')
    Name = models.CharField(max_length=10000,verbose_name=u'名字', default='')
    DeleteFlag=models.IntegerField(default=1,verbose_name='删除状态')
    CreateTime= models.DateTimeField(verbose_name=u'创建时间',  auto_now_add=True)
    UpdateTime= models.DateTimeField(verbose_name=u'更新时间',  auto_now=True)
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")

    class Meta:
        db_table='SpiderItem'
        verbose_name = u'爬虫个体'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Name

class SpiderProperty(models.Model):
    """爬虫属性"""
    Id=models.IntegerField(primary_key=True,verbose_name='Id')
    ItemId=models.IntegerField(verbose_name='ItemId')
    OrderId=models.IntegerField(verbose_name='OrderId')
    PropertyKey = models.CharField(max_length=3000,verbose_name=u'PropertyKey',default='')
    PropertyValue = models.CharField(max_length=3000,verbose_name=u'PropertyValue',default='')
    PropertyBigVal = models.CharField(max_length=12000,verbose_name=u'PropertyBigVal',default='')
    DeleteFlag=models.IntegerField(default=1,verbose_name='删除状态')
    CreateTime= models.DateTimeField(verbose_name=u'创建时间',  auto_now_add=True)
    UpdateTime= models.DateTimeField(verbose_name=u'更新时间',  auto_now=True)
    submission_user=models.CharField(default='alvin',max_length=30,verbose_name="上传用户")
    submission_date=models.DateField(auto_now_add=True,verbose_name="上传时间")

    class Meta:
        db_table='SpiderProperty'
        verbose_name = u'爬虫属性'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.PropertyValue