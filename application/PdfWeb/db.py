#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''

from PdfWeb.models import BookLesson,Chapter,Content,ImageContent,CommonRules,User,UserConfirmString,UserFunction, CommonSubFuncs, Category, UnitDictionary,Article,Comment,Media,MediaSection,Book,Section,\
    CommonCodeMap
from PdfWeb.entitys import HomeInfoItem, NovelInfoItem,ImageInfoItem, NovelIndexItem,\
    NovelContentItem, SpiderSourceEntity, SpiderItemEntity, SpiderPropertyEntity,\
    BookIndexItem,BookContentItem
from django.contrib.auth.hashers import make_password
from PdfWeb import current_log
from django.db import connection

category_map={'learn':2,'tool':3,'blog':4,'audio':5,'video':6,'novel':7,'hiders':8,'image':9}

def select_cnt(select_sql):
    current_log.info(select_sql)
    cursor = connection.cursor()
    cursor.execute(select_sql)
    row = cursor.fetchall()[0]
    return int(row[0])

def select_spider_source(select_sql):
    current_log.info(select_sql)
    cursor = connection.cursor()
    cursor.execute(select_sql)
    result_list=[]
    for row in cursor.fetchall():
        spider_source = SpiderSourceEntity(row[0],row[1],row[2],row[3],row[4],row[5])
        result_list.append(spider_source)
    return result_list

def select_spider_item(select_sql):
    current_log.info(select_sql)
    cursor = connection.cursor()
    cursor.execute(select_sql)
    result_list=[]
    for row in cursor.fetchall():
        spider_item = SpiderItemEntity(row[0],row[1],row[2],row[3],row[4])
        result_list.append(spider_item)
    return result_list

def select_spider_props(select_sql):
    current_log.info(select_sql)
    cursor = connection.cursor()
    cursor.execute(select_sql)
    result_list=[]
    for row in cursor.fetchall():
        spider_prop = SpiderPropertyEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        result_list.append(spider_prop)
    return result_list

def select_spider_prop_max_order_map():
    select_sql = "SELECT ItemId,max(OrderId) FROM spiderproperty WHERE PropertyKey = '章节' group by ItemId"
    current_log.info(select_sql)
    cursor = connection.cursor()
    cursor.execute(select_sql)
    result_map=dict()
    for row in cursor.fetchall():
        result_map[row[0]]=row[1]
    return result_map

def select_novel_infos(select_sql):
    current_log.info(select_sql)
    cursor = connection.cursor()
    cursor.execute(select_sql)
    result_list=[]
    for row in cursor.fetchall():
        novel_info = NovelInfoItem(row[0], row[1], row[2], row[3],row[4],row[5])
        result_list.append(novel_info)
    return result_list

def get_spider_source(source_name):
    select_sql="select * from spidersource where Name= '%s' and DeleteFlag = %s order by Id" %(source_name,1)
    return select_spider_source(select_sql)

def get_spider_item_by_id(item_id):
    select_sql="select * from spideritem where Id= %s order by Id" %(item_id)
    return select_spider_item(select_sql)[0]

def get_spider_item_property(source_id):
    select_sql="select * from spideritem where SourceId= %s and DeleteFlag !=0 order by Id" %(source_id)
    return select_spider_item(select_sql)

def get_spider_item_by_page_no(source_id,page_no,count):
    if page_no == 1:
        begin_no = 0
    else:
        begin_no = (int(page_no)-1) * count
    select_sql="select * from spideritem where SourceId= %s and DeleteFlag !=0 order by Id limit %s,%s" %(source_id,begin_no,count)
    return select_spider_item(select_sql)

def get_spider_property(item_id):
    select_sql="select * from spiderproperty where ItemId= %s order by Id" %(item_id)
    return select_spider_props(select_sql)

def get_spider_property_by_property_id(property_id):
    select_sql="select * from spiderproperty where Id= %s order by Id" %(property_id)
    return select_spider_props(select_sql)[0]

def get_spider_property_by_order_id(item_id,order_id):
    if order_id is None:
        return None
    select_sql="select * from spiderproperty where ItemId= %s and OrderId = %s order by Id" %(item_id,order_id)
    return select_spider_props(select_sql)[0]

def get_spider_property_with_prop_key(item_id,prop_key):
    select_sql="select * from spiderproperty where ItemId= %s and PropertyKey = '%s' order by Id" %(item_id,prop_key)
    return select_spider_props(select_sql)

def get_spider_property_with_max_order_id(item_id,prop_key):
    select_sql="select * from spiderproperty where ItemId= %s and PropertyKey = '%s' order by OrderId desc" %(item_id,prop_key)
    return select_spider_props(select_sql)

def get_spider_property_by_author_name(author_name):
    select_sql="select si.Id,si.Name,sp1.PropertyValue,sp2.PropertyValue,sp3.PropertyValue,sp3.PropertyBigVal FROM spideritem si,spiderproperty sp1,spiderproperty sp2,spiderproperty sp3 where sp1.PropertyValue= '%s' and sp1.PropertyKey = '%s' and sp1.ItemId = si.Id AND si.Id = sp2.ItemId AND sp2.PropertyKey = '简介' AND si.Id = sp3.ItemId AND sp3.PropertyKey = '最新'" %(author_name,'作者')
    return select_novel_infos(select_sql)

def get_image_item_count_by_source_id(source_id):
    select_sql = "SELECT count(*) FROM spideritem WHERE SourceId = %s AND DeleteFlag =2 " %(source_id)
    return select_cnt(select_sql)



def get_prev_order_id(order_id):
    if order_id > 0:
        return order_id -1
    return None

def get_prev_order_no(order_no):
    if order_no > 0:
        return order_no -1
    return 0

def get_category_name_by_category_id(category_id):
    return get_category_by_id(category_id)[0].CategoryName

def get_next_order_id(order_id,max_order_id):
    if order_id < int(max_order_id):
        return order_id +1
    return None

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
    return dict({'p_article':p_article,'article':article,'n_article':n_article,'CategoryName':article.CategoryName},**detail_info)

def get_comments_by_article_id(article_id):
    return get_comments_by_category_id_and_item_id(category_map['blog'],article_id)

def get_comments_by_learn_id(learn_id):
    return get_comments_by_category_id_and_item_id(category_map['learn'],learn_id)

def get_comments_by_novel_id(novel_id):
    return get_comments_by_category_id_and_item_id(category_map['novel'],novel_id)

def get_comments_by_image_id(image_id):
    return get_comments_by_category_id_and_item_id(category_map['image'],image_id)

def get_comments_by_audio_id(audio_id):
    return get_comments_by_category_id_and_item_id(category_map['audio'],audio_id)

def get_comments_by_video_id(video_id):
    return get_comments_by_category_id_and_item_id(category_map['video'],video_id)

def get_comments_by_category_id_and_item_id(category_id,item_id):
    return Comment.objects.filter(CategoryId=category_id,ItemId=item_id,DeleteFlag=0)

def get_comments_by_category_key_and_item_id(category_key,item_id):
    return Comment.objects.filter(CategoryId=category_map[category_key],ItemId=item_id,DeleteFlag=0)


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

def get_learn_category_type_info():
    return get_category_by_key('learn')

def get_audio_category_type_info():
    return get_category_by_key('music')

def get_common_tool_type_info():
    return get_category_by_key('tool')

def get_blog_category_type_info():
    return get_category_by_key('blog')

def get_novel_category_type_info():
    return get_category_by_key('novel')
#     category_list = get_category_by_key('novel')
#     for category in category_list:
#         category.CategoryId = category.CategoryId - 100
#     return category_list

def get_image_category_type_info():
    return get_category_by_key('image')
#     category_list = get_category_by_key('image')
#     for category in category_list:
#         category.CategoryId = category.CategoryId - 200
#     return category_list

def get_blog_tag_category_type_info():
    return get_category_by_key('blogtag')

def get_category_by_id(category_id):
    return Category.objects.filter(DeleteFlag=0,CategoryId=category_id)

def get_category_by_father(category_id):
    return Category.objects.filter(DeleteFlag=0,CategoryFather=category_id)

def get_category_by_key(category_key):
    category=Category.objects.get(CategoryName=category_key,DeleteFlag=0)
    return get_category_by_father(category.CategoryId)

def del_section_by_id(section_id):
    section = Section.objects.filter(Id=section_id)[0]
    section.DeleteFlag = 1
    section.save(update_fields=['DeleteFlag'])
    return section.BookId

def upd_section(section):
    section.save()

def ins_section(section_dict):
    return Section.objects.create(**section_dict)

def del_book_by_id(book_id):
    book = Book.objects.filter(Id=book_id)[0]
    book.DeleteFlag = 1
    book.save(update_fields=['DeleteFlag'])
    return book.CategoryId

def upd_book(book):
    book.save()

def ins_book(book_dict):
    return Book.objects.create(**book_dict)

def get_book_count_by_category_id(category_id):
    return Book.objects.filter(DeleteFlag=0,CategoryId=category_id).count()

def get_book_by_id(book_id):
    return Book.objects.filter(DeleteFlag=0,Id=book_id)[0]

def get_book_infos_by_author(author_name):
    return Book.objects.filter(DeleteFlag=0,Author=author_name)

def get_book_by_category_id(category_id,page_no,page_count):
    page_no = int(page_no)
    start_row=page_no*page_count-page_count
    end_row=page_no*page_count
    total_count=get_book_count_by_category_id(category_id)
    if end_row > total_count:
        end_row=total_count
    return Book.objects.filter(DeleteFlag=0,CategoryId=category_id)[start_row:end_row]

def get_book_sections_by_book_id(book_id):
    return Section.objects.filter(DeleteFlag=0,BookId=book_id).order_by("OrderNo")

def get_max_book_section_order_no(book_id):
    res=list(get_book_sections_by_book_id(book_id))
    if res:
        return res[-1].OrderNo
    return -1

def get_book_section_by_id(section_id):
    return Section.objects.filter(DeleteFlag=0,Id=section_id)[0]

def get_book_section_by_order_no(book_id,order_no):
    if order_no is None:
        return None
    if order_no < 0:
        return ''
    return Section.objects.filter(DeleteFlag=0,BookId=book_id,OrderNo=order_no)[0]

def get_booksections_by_id(book_id):
    book=get_book_by_id(book_id)
    sections=get_book_sections_by_book_id(book_id)
    return BookIndexItem(book,sections)

def get_book_content_include_prev_next_page(book_id,section_order_no, max_section_order_no):
    max_section_order_no = int(max_section_order_no)
    section_order_no=int(section_order_no)
    section = get_book_section_by_order_no(book_id,section_order_no)
    prev_order_id = get_prev_order_id(section_order_no)
    next_order_id = get_next_order_id(section_order_no, max_section_order_no)
    return BookContentItem(book_id,section,prev_order_id,next_order_id)

def get_book_distinct_id(section):
    if section is None:
        return None
    return section.OrderNo

def get_media_by_category_id(category_id,page_no,page_count):
    page_no = int(page_no)
    start_row=page_no*page_count-page_count
    end_row=page_no*page_count
    total_count=get_media_count_by_category_id(category_id)
    if end_row > total_count:
        end_row=total_count
    return Media.objects.filter(DeleteFlag=0,CategoryId=category_id)[start_row:end_row]

def get_media_count_by_category_id(category_id):
    return Media.objects.filter(DeleteFlag=0,CategoryId=category_id).count()

def get_media_by_id(media_id):
    return Media.objects.get(DeleteFlag=0,Id=media_id)

def get_media_section_by_media_id_order_no(media_id,order_no):
    return MediaSection.objects.filter(DeleteFlag=0,MediaId=media_id,OrderNo=order_no)[0]

def get_media_sections_by_media_id(media_id):
    return MediaSection.objects.filter(DeleteFlag=0,MediaId=media_id)

def get_media_section_count_by_media_id(media_id):
    return MediaSection.objects.filter(DeleteFlag=0,MediaId=media_id).count()

def get_common_code_type(code_type):
    return CommonCodeMap.objects.filter(DeleteFlag=0,CodeType=code_type)

def get_link_directory_map():
    common_codes= get_common_code_type("LinkDirectory")
    link_map=dict()
    for common_code in common_codes:
        link_map[common_code.TypeKey]=common_code.TypeVal
    return link_map

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


#start not in use
def get_novel_source():
    return get_spider_source('小说')

def get_novel_info_item(item_id):
    select_sql = "SELECT si.Id,si.Name,sp1.PropertyValue,sp2.PropertyValue,sp3.PropertyValue,sp3.PropertyBigVal FROM spideritem si,spiderproperty sp1,spiderproperty sp2,spiderproperty sp3 WHERE si.Id = %s AND si.DeleteFlag !=0 AND si.Id = sp1.ItemId AND sp1.PropertyKey = '作者' AND si.Id = sp2.ItemId AND sp2.PropertyKey = '简介' AND si.Id = sp3.ItemId AND sp3.PropertyKey = '最新'" %(item_id)
    return select_novel_infos(select_sql)[0]

def get_novel_infos_by_author(author_name):
    return get_spider_property_by_author_name(author_name)

def get_novel_items_by_source_id(source_id,page_no,count):
    if page_no == 1:
        begin_no = 0
    else:
        begin_no = (int(page_no)-1) * count
    select_sql = "SELECT si.Id,si.Name,sp1.PropertyValue,sp2.PropertyValue,sp3.PropertyValue,sp3.PropertyBigVal FROM spideritem si,spiderproperty sp1,spiderproperty sp2,spiderproperty sp3 WHERE si.SourceId = %s AND si.DeleteFlag !=0 AND si.Id = sp1.ItemId AND sp1.PropertyKey = '作者' AND si.Id = sp2.ItemId AND sp2.PropertyKey = '简介' AND si.Id = sp3.ItemId AND sp3.PropertyKey = '最新' limit %s,%s" %(source_id,begin_no,count)
    return select_novel_infos(select_sql)

def get_novel_item_count_by_source_id(source_id):
    select_sql = "SELECT count(*) FROM spideritem WHERE SourceId = %s AND DeleteFlag !=0 " %(source_id)
    return select_cnt(select_sql)
    
def get_novel_contents_by_item_id(item_id):
    novel_info = get_novel_info_item(item_id)
    novel_contents = get_spider_property_with_prop_key(item_id, '章节')
    return NovelIndexItem(novel_info,novel_contents)

def get_novel_content_include_prev_next_page(property_id,last_upd_content_order_id):
    novel_chapter = get_spider_property_by_property_id(property_id)
    novel_item_id = novel_chapter.ItemId
    novel_order_id = novel_chapter.OrderId
    prev_order_id = get_prev_order_id(novel_order_id)
    next_order_id = get_next_order_id(novel_order_id, last_upd_content_order_id)
    prev_chapter = get_spider_property_by_order_id(novel_item_id, prev_order_id)
    next_chapter = get_spider_property_by_order_id(novel_item_id, next_order_id)
    return NovelContentItem(novel_item_id,novel_chapter,get_novel_spider_id(prev_chapter),get_novel_spider_id(next_chapter))

def get_image_content_info(item_id):
    spider_item = get_spider_item_by_id(item_id)
    spider_props = get_spider_property(item_id)
    return ImageInfoItem(item_id,spider_item.Name,spider_props)


def get_novel_spider_id(novel_spider_property):
    if novel_spider_property is None:
        return None
    return novel_spider_property.Id

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

#end not in use