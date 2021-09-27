#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from PdfWeb import db,entitys,current_log
from PdfWeb.entitys import HomeIndexItem, PageInfoItem
from tools import common_tools, common_converter, common_formater, common_coder,common_calculator,common_executer
import datetime
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # 翻页相关模块

html_no_rules=db.get_common_rules_by_type_and_rule('html5', 'no_text')
html_clean_rules=db.get_common_rules_by_type_and_rule('html5', 'clean_text')
html_child_rules=db.get_common_rules_by_type_and_rule('html5', 'child_text')
html_children_rules=db.get_common_rules_by_type_and_rule('html5', 'children_text')
html_dirty_rules=db.get_common_rules_by_type_and_rule('html5', 'dirty_text')
html_no_tags=entitys.convert_common_rules_to_tag_dict(html_no_rules)
html_clean_tags=entitys.convert_common_rules_to_tag_dict(html_clean_rules)
html_child_tags=entitys.convert_common_rules_to_tag_dict(html_child_rules)
html_children_tags=entitys.convert_common_rules_to_tag_dict(html_children_rules)
html_dirty_tags=entitys.convert_common_rules_to_tag_dict(html_dirty_rules)
font_rules=db.get_common_rules_by_type('font')
font_tags=entitys.convert_common_rules_to_tag_dict(font_rules)
learn_menu_list = db.get_book_lesson_type_info()
tool_menu_list = db.get_common_tool_type_info()
blog_category_list= db.get_blog_category_type_info()
novel_source_list = db.get_novel_category_type_info()
image_source_list = db.get_image_category_type_info()

def get_pages(begin_no,end_no,category_id,num_pages):
    pages = []
    pages.append(PageInfoItem("首页",F'{category_id}/1'))
    for i in range(begin_no, end_no):
        page_no=i+1
        page=PageInfoItem(page_no,F'{category_id}/{page_no}')
        pages.append(page)
    pages.append(PageInfoItem("末页",F'{category_id}/{num_pages}'))
    return pages

def pages_help(page,num_pages,category_id,maxpage):
    '''
    Paginator Django数据分页优化
        使数据分页列表处显示规定的页数
    :param page: 当前页码
    :param num_pages: 总页数
    :param category_id:分类Id
    :param maxpage: 列表处最多显示的页数
    :return:
    '''
    
    if page is None:#首页时page=None
        p=1
    else:
        p = int(page)
    # print(num_pages,p,maxpage)
    offset = num_pages-p
    if num_pages > maxpage and offset <= maxpage and p>= maxpage:
        #假设100页 100-98=2,页尾处理
        # 结果小于规定数但是当前页大于规定页数
        # print("结果小于规定数但是当前页大于规定页数",[i + 1 for i in range(num_pages - maxpage, num_pages)])
        return get_pages(num_pages - maxpage, num_pages,category_id,num_pages)
    elif num_pages > maxpage and offset >= maxpage and p <= maxpage:
        #假设100页 100-2=98，页头
        # 结果小于规定数但是当前页大于规定页数
        # print("结果小于规定数但是当前页大于规定页数",[i + 1 for i in range(maxpage)])
        return get_pages(0, maxpage,category_id,num_pages)
    elif num_pages <= maxpage:
        #假设3页  3<6，总页数很少，少于规定页数
        # 当前页码数小于规定数
        # print("当前页码数小于规定数",[i + 1 for i in range(num_pages)])
        return get_pages(0, num_pages,category_id,num_pages)
    else:
        # 正常页数分配
        # print("正常页数分配",[i + 1 for i in range(p - int(maxpage / 2), p + int(maxpage / 2))])
        return get_pages(p - int(maxpage / 2), p + int(maxpage / 2),category_id,num_pages)

def content_infos_to_text(content_infos):
    text_list=[]
    for content_info in content_infos:
        if content_info.ElementTag not in ['image','line']:
            text_str = content_info.Text.replace("BOLD[","").replace("]BOLD","").replace("BLUE_BG[","").replace("]BLUE_BG","")
            text_list.append(text_str)
    return "\n".join(text_list)

def get_home_index():
    user_funcs = db.get_user_function('a', 1)
    content_list=[]
    for i, user_func in enumerate(user_funcs):
        func_str =user_func.FunctionStr
        title = func_str.split("/")[1].capitalize()
        temp_str=F'<div class="col-md-4 column"><h1>{title}</h1><p>{title} website!</p><p><a class="btn" href="{func_str}">View details</a></p></div>'
        check_id = i+1
        if check_id % 3 ==1:
            temp_str=F'<div class="row clearfix">{temp_str}'
        elif check_id % 3 ==0:
            temp_str=F'{temp_str}</div>'
        content_list.append(temp_str)
    return "".join(content_list)

def get_tool_val_list():
    tool_val_list = []
    for common_tool_type in tool_menu_list:
        tool_items = db.get_common_sub_func_info(common_tool_type.CategoryId)
        id_name = common_tool_type.CategoryValue1.replace('#', '')
        item = HomeIndexItem(id_name, common_tool_type.CategoryName, tool_items)
        tool_val_list.append(item)
    return tool_val_list

def get_tool_home_index():
    keys = ['menu_list','val_list']
    tool_val_list = get_tool_val_list()
    vals = [tool_menu_list,tool_val_list]
    return common_tools.create_map(keys,vals)

def get_tool_func(tool,method,inputarea,passkey):
    if tool in ("codetool","converttool"):
        return eval(tool)(method,inputarea,passkey)
    return eval(tool)(method,inputarea)
    
def jsontool(method,inputval):
    func = getattr(common_formater,method)
    return func(inputval)
    
def codetool(method,inputval,passkey):
    func = getattr(common_coder, method)
    need_key_methods=['encode2hmacsha1','encode2hmacmd5','encode2hmacsha224','encode2hmacsha256','encode2hmacsha384','encode2hmacsha512','encode2rc4','decode2rc4','encode2aes','decode2aes','encode2des3','decode2des3','encode2rsa','decode2rsa','encode2des','decode2des']
    if method in need_key_methods:
        return func(inputval,passkey)
    return func(inputval)

def codingtool(method,inputval):
    func = getattr(common_coder,method)
    return func(inputval)

def ziptool(method,inputval):
    func = getattr(common_formater,method)
    return func(inputval)
def converttool(method,inputval,spec_val):
    func = getattr(common_converter,method)
    need_key_methods=["first_ones_lower","last_ones_lower","first_ones_upper","last_ones_upper","delete_first_ones","delete_last_ones","add_first_specs","add_last_specs"]
    if method in need_key_methods:
        return func(inputval,spec_val)
    return func(inputval)
def calctool(method,inputval):
    func = getattr(common_calculator,method)
    return func(inputval)
def runtool(method,inputval):
    func = getattr(common_executer,method)
    return func(list(inputval.split("\n")))
def strtool(method,inputval):
    func = getattr(common_converter,method)
    return func(inputval)

def get_novel_sources():
    return db.get_novel_source()

def get_image_home_index():
    return get_image_home_list(15,1)

def get_image_home_list(source_id,page_no):
    keys = ['image_source_list','contacts','pages']
    image_info_list = db.get_spider_item_by_page_no(source_id,page_no,30)
    image_cnt = db.get_image_item_count_by_source_id(source_id)
    current_log.info(image_source_list)
    current_log.info(image_cnt)
    max_page = image_cnt//30
    if image_cnt % 30 != 0:
        max_page = max_page+1
    pages = pages_help(page_no, max_page, source_id, 6)
    vals=[image_source_list,image_info_list,pages]
    return common_tools.create_map(keys, vals)

def get_image_content_info(item_id):
    keys = ['image_source_list','image_content_info']
    content_info=db.get_image_content_info(item_id)
    vals=[image_source_list,content_info]
    return common_tools.create_map(keys, vals)

def get_novel_home_index():
    return get_novel_home_list(1, 1)

def get_novel_home_list(source_id,page_no):
    keys = ['novel_source_list','contacts','pages']
    novel_info_list = db.get_novel_items_by_source_id(source_id,page_no,20)
    novel_cnt = db.get_novel_item_count_by_source_id(source_id)
    current_log.info(novel_source_list)
    current_log.info(novel_cnt)
    max_page = novel_cnt//20
    if novel_cnt % 20 != 0:
        max_page = max_page+1
    pages = pages_help(page_no, max_page, source_id, 6)
    vals=[novel_source_list,novel_info_list,pages]
    return common_tools.create_map(keys, vals)

def get_novel_menu_info(item_id):
    keys = ['novel_source_list','novel_menu_info','action']
    novel_info = db.get_novel_contents_by_item_id(item_id)
    vals= [novel_source_list,novel_info,'menu']
    return common_tools.create_map(keys, vals)

def get_novel_content_info(prop_id,last_upd_content_ord_id):
    keys = ['novel_source_list','novel_content_info','last_upd_content_ord_id','action']
    content_info=db.get_novel_content_include_prev_next_page(prop_id, last_upd_content_ord_id)
    vals=[novel_source_list,content_info,last_upd_content_ord_id,'content']
    return common_tools.create_map(keys, vals)

def get_novel_infos_by_author(item_id):
    novel_info = db.get_novel_contents_by_item_id(item_id)
    author_name=novel_info.novel_info.author
    keys = ['novel_source_list','item_id','author_name','novel_info_list','action']
    novel_info_list = db.get_novel_infos_by_author(author_name)
    vals = [novel_source_list,item_id,author_name,novel_info_list,'author']
    return common_tools.create_map(keys, vals)    

def get_blog_home_index():
    return get_blog_home_list(0, 1)

def get_blog_home_list(category_id,page_no):
    keys = ['category_list','article_list','contacts','hot_article_list','pages']
    if category_id == 0:
        article_list=db.get_articles_by_type()
    else:
        article_list=db.get_articles_by_category_id(category_id)
    paginator = Paginator(article_list, 8)  # 第二个参数是每页显示的数量
    try:
        contacts = paginator.page(page_no)
    except PageNotAnInteger:  # 若不是整数则跳到第一页
        contacts = paginator.page(1)
    except EmptyPage:  # 若超过了则最后一页
        contacts = paginator.page(paginator.num_pages)
    #优化数据翻页
    pages = pages_help(page_no,paginator.num_pages,category_id,6)
    if category_id ==0 :
        hot_article_list=db.get_articles_order_by_click_count()[0:10]
    else:
        hot_article_list=db.get_articles_by_category_id_order_by_click_count(category_id)[0:10]
    vals=[blog_category_list,article_list,contacts,hot_article_list,pages]
    return common_tools.create_map(keys,vals)

def del_blog_article_by_id(article_id):
    db.del_article_by_article_id(article_id)
    
def ins_blog_article(article_dict):
    return db.ins_article(article_dict)
    
def upd_blog_article(article):
    db.upd_article(article)
    return article

def get_blog_article(article_id):
    result = db.get_page_articles_by_id(article_id)
    comments = db.get_comments_by_article_id(article_id)
    current_log.info(result)
    current_log.info(blog_category_list)
    result['blog_category_list'] = blog_category_list
    result['comments'] = comments
    return result

def get_blog_article_info(author_id):
    result = db.get_blog_articles_info_by_author_id(author_id)
    result['blog_category_list'] = blog_category_list
    return result

def get_learn_val_list():
    learn_val_list = []
    for book_lesson_type in learn_menu_list:
        index_list = db.get_book_lesson_image_info(book_lesson_type.CategoryId)
        id_name = book_lesson_type.CategoryValue1.replace('#','')
        item = HomeIndexItem(id_name,book_lesson_type.CategoryName,index_list)
        learn_val_list.append(item)
    return learn_val_list

def get_learn_home_index():
    keys = ['menu_list','val_list']
    vals = [learn_menu_list,get_learn_val_list()]
    return common_tools.create_map(keys,vals)

def get_menus(book_type_id):
    book_lessons= db.get_book_lesson_info(book_type_id)
    menus = []
    for book_lesson in book_lessons:
        menus.append(book_lesson.LessonHref.replace("/learn/","").replace("/index",""))
    return menus

def get_restful(book_lesson_id,lesson_key):
    chapters = db.get_chapter_infos(book_lesson_id)
    restfuls = []
    for chapter in chapters:
        single_href=chapter.Href.replace(F"learn/{lesson_key}/","")
        restfuls.append(single_href)
    return restfuls

def get_user_by_name(user_name):
    users=db.get_user_by_name(user_name)
    if users:
        return users[0]
    return None

def get_user_by_email(mail):
    users=db.get_user_by_email(mail)
    if users:
        return users[0]
    return None

def get_user_by_id(user_id):
    return db.get_user_by_id(user_id)[0]

def new_user(user_name,password,email,sex,detail,logo,permission):
    return db.create_user(user_name, password, email, sex,detail, logo,permission)

def update_user(user_id,user_name,email,sex,detail,logo):
    return db.update_user(user_id,user_name, email, sex,detail, logo)

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = make_password(now,user.Name,'pbkdf2_sha256')
    db.create_confirm_msg(user, code)
    return code

def delete_by_confirm(confirm):
    users = db.get_user_by_id(confirm.User_Id)
    users.update(DeleteFlag = 1)

def update_user_by_confirm(confirm):
    users = db.get_user_by_id(confirm.User_Id)
    users.update(DeleteFlag = 0)
    confirm.delete()

def get_confirm(code):
    confirms = db.get_confirm_item(code)
    if confirms:
        return confirms[0]
    return None

def get_chapter_headers(book_lesson_id):
    return db.get_chapter_infos(book_lesson_id)

def get_chapter_contents(chapter_id):
    return db.get_content_infos(chapter_id)
    
def get_chapters(book_lesson_id,chapter_href):
    header_list=get_chapter_headers(book_lesson_id)
    chapter_infos=db.get_chapter_by_href(chapter_href)
    chapter_info=chapter_infos[0]
    detail_list=get_chapter_contents(chapter_info.Id)
    content_html=convert_details_to_html(detail_list)
    keys = ['val_list','header_list','content_html']
    vals = [get_learn_val_list(),header_list,content_html]
    return common_tools.create_map(keys, vals)

def convert_attribute_map_to_str(content_detail):
    if content_detail.AttributeMap !="{}":
        attribute_map=eval(content_detail.AttributeMap)
        attribute_str=""
        for key,value in attribute_map.items():
            str_value=value
            if common_tools.is_list(value):
                str_value=" ".join(value)
            attribute_str=F'{attribute_str} {key}="{str_value}"'
        return attribute_str
    return ""

def convert_font_to_html(str_text):
    text_html=str_text
    for val in font_tags.keys():
        font1_list = text_html.split(F'{val}[')
        font2_list = text_html.split(F']{val}')
        if font1_list and font2_list and len(font1_list) == len(font2_list) and len(font1_list) >1:
            for num in range(len(font1_list)):
                if num %2 ==1:
                    font1_list[num]=font1_list[num].lstrip()
                    text_html=font_tags[val].RulesDescription.join(font1_list)
                else:
                    font2_list[num]=font2_list[num].rstrip()
                    text_html=font_tags[val].RulesText.join(font2_list)
    return text_html

def convert_html_text(content_detail):
    tag_name=content_detail.ElementTag
    text_html=convert_font_to_html(content_detail.Text)
    html_text=common_converter.str2htmlspec(text_html)
    if tag_name == 'pre':
        html_text=content_detail.Text.replace("<","&lt;")
    return html_text

def convert_child_html_text(content_detail,common_rule):
    childs_text=content_detail.Text.split("\n")
    child_tag=common_rule.RulesDescription
    html_text=""
    for child_str in childs_text:
        text_html=convert_font_to_html(child_str)
        child_str=common_converter.str2htmlspec(text_html)
        html_text=F'{html_text}<{child_tag}>{child_str}</{child_tag}>'
    return html_text

def convert_common_html_text(childs_list,parent_tag,child_tag):
    child_html=""
    for childs_str in childs_list:
        text_html=convert_font_to_html(childs_str)
        childs_str=common_converter.str2htmlspec(text_html)
        child_html=F'{child_html}<{child_tag}>{childs_str}</{child_tag}>'
    return F'<{parent_tag}>{child_html}</{parent_tag}>'

def convert_no_text(content_detail,common_rule):
    tag_name=common_rule.RulesDescription
    attribute_str=convert_attribute_map_to_str(content_detail)
    return F'<{tag_name}{attribute_str}/>'

def convert_clean_text(content_detail):
    tag_name=content_detail.ElementTag
    html_text=convert_html_text(content_detail)
    attribute_str=convert_attribute_map_to_str(content_detail)
    return F'<{tag_name}{attribute_str}>{html_text}</{tag_name}>'

def convert_child_text(content_detail,common_rule):
    tag_name=content_detail.ElementTag
    html_text=convert_child_html_text(content_detail,common_rule)
    attribute_str=convert_attribute_map_to_str(content_detail)
    return F'<{tag_name}{attribute_str}>{html_text}</{tag_name}>'

def convert_children_text(content_detail,common_rule):
    tag_name=content_detail.ElementTag
    childs_text=content_detail.Text.split("\n")
    child_tags=common_rule.RulesDescription.split(":")
    body_tag=child_tags[0]
    parent_tag=child_tags[1]
    header_tag=child_tags[2]
    detail_tag=child_tags[-1]
    header_list=childs_text[0].split("\t")
    header_str=convert_common_html_text(header_list,parent_tag,header_tag)
    detail_list = []
    for child_str in childs_text[1:]:
        detail_str=convert_common_html_text(child_str.split("\t"), parent_tag, detail_tag)
        detail_list.append(detail_str)
    detail_strs="".join(detail_list)
    attribute_str=convert_attribute_map_to_str(content_detail)
    return F'<{tag_name}{attribute_str}><{body_tag}>{header_str}{detail_strs}</{body_tag}></{tag_name}>'

def convert_dirty_text(content_detail,common_rule):
    child_tags=common_rule.RulesDescription.split(":")
    html_text=""
    main_id=int(common_rule.RulesText)-1
    main_tag=child_tags[main_id]
    for child_tag in child_tags[::-1]:
        attribute_str=""
        if child_tag == main_tag:
            attribute_str=convert_attribute_map_to_str(content_detail)
        tag_id= child_tag.find(".")
        if tag_id >-1:
            real_tag = child_tag[tag_id+1:]
            html_text = F'<{real_tag}{attribute_str}>'
        else:
            html_text= F'<{child_tag}{attribute_str}>{html_text}</{child_tag}>'
    return html_text
            
def convert_details_to_html(detail_list):
    detail_html_list=[]
    for content_detail in detail_list:
        tag_name = content_detail.ElementTag
        detail_html=""
        if tag_name in html_no_tags.keys():
            detail_html=convert_no_text(content_detail,html_no_tags[tag_name])
        elif tag_name in html_clean_tags.keys():
            detail_html=convert_clean_text(content_detail)
        elif tag_name in html_child_tags.keys():
            detail_html=convert_child_text(content_detail, html_child_tags[tag_name])
        elif tag_name in html_children_tags.keys():
            detail_html=convert_children_text(content_detail, html_children_tags[tag_name])
        elif tag_name in html_dirty_tags.keys():
            detail_html=convert_dirty_text(content_detail, html_dirty_tags[tag_name])
        detail_html_list.append(detail_html)
    return "\n".join(detail_html_list)

