#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''

from PdfWeb.models import BookLesson,Chapter,Content,ImageContent,CommonRules,User,UserConfirmString,UserFunction, CommonSubFuncs, Category, UnitDictionary,Article,Comment
from PdfWeb.entitys import HomeInfoItem
from django.contrib.auth.hashers import make_password
from PdfWeb import current_log

def get_articles_by_type(article_type='2'):
    return Article.objects.filter(Type=article_type,DeleteFlag=0).order_by('CreateTime')

def get_article_by_id(article_id):
    return Article.objects.get(Id=article_id,DeleteFlag=0)

def get_articles_by_author_id(author_id):
    return Article.objects.filter(AuthorId=author_id,DeleteFlag=0).order_by('CreateTime')

def get_articles_order_by_click_count():
    return Article.objects.filter(DeleteFlag=0).order_by('-Click')

def get_articles_by_category_id_order_by_click_count(category_id):
    return Article.objects.filter(CategoryId=category_id,DeleteFlag=0).order_by('-Click')

def get_articles_by_category_id(category_id):
    return Article.objects.filter(CategoryId=category_id,DeleteFlag=0).order_by('CreateTime')

def get_articles_group_by_tag(articles):
    tag_dict = {}
    for article in articles:
        if article.TagName in tag_dict:
            tag_dict[article.TagName].append(article)
        else:
            tag_dict[article.TagName]=[article]
    return tag_dict

def get_articles_group_by_month(articles):
    month_dict={}
    for article in articles:
        year_month = format(article.UpdateTime,'%Y-%m')
        if year_month in month_dict:
            month_dict[year_month].append(article)
        else:
            month_dict[year_month]=[article]
    return month_dict

def get_blog_articles_info_by_author_id(author_id):
    articles=get_articles_by_author_id(author_id)
    author = get_user_by_id(author_id)[0]
    tag_dict=get_articles_group_by_tag(articles)
    month_dict=get_articles_group_by_month(articles)
    view_count = 0 
    article_cnt = len(articles)
    for article in articles:
        view_count += article.Click
    return {'author':author,'tag':tag_dict,'month':month_dict,'articles':articles,'article_cnt':article_cnt,'view_count':view_count}

def del_article_by_article_id(article_id):
    article = Article.objects.filter(Id=article_id)
    article.DeleteFlag = 1
    article.save(update_fields=['DeleteFlag'])
    
def ins_article(article_dict):
    return Article.objects.create(**article_dict)

def upd_article(article):
    article.save()

def get_page_articles_by_id(article_id):
    article=get_article_by_id(article_id)
    article.increase_article_click()
    detail_info=get_blog_articles_info_by_author_id(article.AuthorId)
    articles = detail_info['articles']
    current_log.info(articles)
    p_article=None
    n_article=None
    for i in range(0,len(articles)):
        if articles[i].Id == article.Id:
            pre_id = i-1
            next_id = i+1
            if pre_id >=0:
                p_article=articles[pre_id]   
            if next_id < len(articles):
                n_article=articles[next_id]
    return dict({'p_article':p_article,'article':article,'n_article':n_article},**detail_info)

def get_comments_by_article_id(article_id):
    return Comment.objects.filter(ArticleId=article_id,DeleteFlag = 0)

def get_user_by_name(user_name):
    return User.objects.filter(Name=user_name)

def get_user_by_email(mail):
    return User.objects.filter(Email=mail)

def get_user_by_id(user_id):
    return User.objects.filter(Id=user_id)

def get_user_function(group_key,role_id):
    return UserFunction.objects.filter(GroupKey=group_key,RoleId=role_id,DeleteFlag=0)

def create_user(user_name,password,email,sex,detail,logo,permission):
    password1=make_password(password,user_name,'pbkdf2_sha256')
    User.objects.create(Name = user_name,Password = password1,Email = email,Logo=logo,Sex = sex,Detail=detail,Permissions = permission)
    user = get_user_by_name(user_name)
    if user:
        return user[0]
    return None

def update_user(user_id,user_name,email,sex,detail,logo):
    User.objects.update(Id=user_id,Name=user_name,Email = email,Logo=logo,Sex = sex,Detail=detail)
    user = get_user_by_id(user_id)
    if user:
        return user[0]
    return None
    
def create_confirm_msg(user,code):
    UserConfirmString.objects.create(code=code, User_Id=user.Id)

def get_confirm_item(code):
    return UserConfirmString.objects.filter(code=code)

def get_common_sub_func_by_id(common_type_id):
    return CommonSubFuncs.objects.filter(DeleteFlag=0,CommonMainType_Id=common_type_id)

def get_book_lesson_by_id(book_lesson_id):
    return BookLesson().objects.get(pk=book_lesson_id,DeleteFlag=0)

def get_content_by_id(content_id):
    return Content().objects.get(pk=content_id,DeleteFlag=0)

def get_chapter_by_id(chapter_id):
    return Chapter().objects.get(pk=chapter_id,DeleteFlag=0)

def get_image_content_by_id(image_id):
    return ImageContent.objects.get(pk=image_id,DeleteFlag=0)

def get_chapter_by_href(href):
    return Chapter.objects.filter(Href=href,DeleteFlag=0).order_by('ChapterNo')

def get_book_lesson_type_info():
    category=Category.objects.get(CategoryName='learn',DeleteFlag=0)
    return Category.objects.filter(DeleteFlag=0,CategoryFather=category.CategoryId)

def get_common_tool_type_info():
    category=Category.objects.get(CategoryName='tool',DeleteFlag=0)
    return Category.objects.filter(DeleteFlag=0,CategoryFather=category.CategoryId)

def get_blog_category_type_info():
    category=Category.objects.get(CategoryName='blog',DeleteFlag=0)
    return Category.objects.filter(DeleteFlag=0,CategoryFather=category.CategoryId)

def get_blog_tag_category_type_info():
    category=Category.objects.get(CategoryName='blogtag',DeleteFlag=0)
    return Category.objects.filter(DeleteFlag=0,CategoryFather=category.CategoryId)

def get_category_by_id(category_id):
    return Category.objects.filter(DeleteFlag=0,CategoryId=category_id)

def get_book_lesson_info(book_lesson_type_id):
    return BookLesson.objects.filter(BookLessonType_Id=book_lesson_type_id,DeleteFlag=0)

def get_chapter_infos(book_lesson_id):
    return Chapter.objects.filter(BookLesson_Id=book_lesson_id,DeleteFlag=0).order_by('ChapterNo')

def get_content_infos(chapter_id):
    return Content.objects.filter(Chapter_Id=chapter_id,DeleteFlag=0).order_by('OrderIndex')
    
def get_image_content_infos(image_id):
    return ImageContent.objects.filter(Id=image_id,DeleteFlag=0)

def get_book_lesson_image_info(book_lesson_type_id):
    book_lessons=get_book_lesson_info(book_lesson_type_id)
    book_lesson_image_list=[]
    for book_lesson in book_lessons:
        image_content = get_image_content_infos(book_lesson.ImageContent_Id)
        home_info_item=HomeInfoItem(book_lesson,image_content[0])
        book_lesson_image_list.append(home_info_item)
    return book_lesson_image_list

def get_common_sub_func_info(common_tool_type_id):
    tool_items = get_common_sub_func_by_id(common_tool_type_id)
    items_list = []
    for tool_item in tool_items:
        items_list.append(tool_item)
    return items_list

def get_common_rules():
    return CommonRules.objects.filter(DeleteFlag=0)

def get_common_rules_by_type(rule_type):
    return CommonRules.objects.filter(TypeKey=rule_type,DeleteFlag=0)

def get_common_rules_by_type_and_rule(rule_type,rules):
    return CommonRules.objects.filter(TypeKey=rule_type,Rules=rules,DeleteFlag=0)

def get_unit_dictionary_by_conversion_type(conversion_type):
    return UnitDictionary.objects.filter(ConversionType=conversion_type,DeleteFlag=0)

def get_unit_dictionary():
    return UnitDictionary.objects.filter(DeleteFlag=0)