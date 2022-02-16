#-*- encoding:UTF-8 -*-
'''
Created on 2019/12/28

@author: xcKev
'''

from PdfWeb.models import CommonRules,User,UserConfirmString,UserFunction, CommonSubFuncs, Category, UnitDictionary,Article,Comment,Media,MediaSection,Book,Section,\
    CommonCodeMap
from PdfWeb.entitys import BookIndexItem,BookContentItem
from django.contrib.auth.hashers import make_password
from PdfWeb import current_log

category_map={'learn':2,'tool':3,'blog':4,'audio':5,'video':6,'novel':7,'hiders':8,'image':9}


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

def get_comment_by_category_id_and_comment_id(category_id,comment_id):
    return Comment.objects.filter(CategoryId=category_id,Id=comment_id,DeleteFlag=0)[0]

def ins_comment_by_category_key_and_item_id(category_key,item_id,content,user_id,user_name):
    return Comment.objects.create(CategoryId= category_map[category_key],ItemId=item_id,Content=content,AuthorId=user_id,AuthorName=user_name)

def del_comment_by_id(category_key,comment_id):
    category_id = category_map[category_key]
    comment = get_comment_by_category_id_and_comment_id(category_id,comment_id)
    comment.DeleteFlag = 1
    comment.save(update_fields=['DeleteFlag'])
    return comment

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

def get_video_category_type_info():
    return get_category_by_key('video')

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

def get_media_section_by_id(section_id):
    return MediaSection.objects.get(DeleteFlag=0,Id=section_id)

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