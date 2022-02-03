#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from PdfWeb import db,entitys,current_log
from PdfWeb.entitys import HomeIndexItem, PageInfoItem
from alvintools import common_tools, common_converter, common_formater, common_coder,common_calculator,common_executer,\
    common_filer
import datetime
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # 翻页相关模块
from PdfWeb.settings import MEDIA_ROOT
from alvinwritecreater import pdfwriter
from alvinwritecreater.fileswriter import SimpleFileWriter
from alvinreadparser.markdownreader import MarkDownReader


category_map={
    "learn":db.get_learn_category_type_info(),
    "novel":db.get_novel_category_type_info(),
    "image":db.get_image_category_type_info(),
    "audio":db.get_audio_category_type_info(),
    "video":db.get_video_category_type_info(),
    }

tool_menu_list = db.get_common_tool_type_info()
blog_category_list= db.get_blog_category_type_info()
link_map = db.get_link_directory_map()

def get_pages(begin_no,end_no,category_id,num_pages):
    pages = []
    pages.append(PageInfoItem("首页",F'{category_id}/1'))
    if begin_no >0:
        prev_page_no = begin_no 
        pages.append(PageInfoItem("上一页",F'{category_id}/{prev_page_no}'))
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
    elif num_pages <= maxpage:
        #假设3页  3<6，总页数很少，少于规定页数
        # 当前页码数小于规定数
        # print("当前页码数小于规定数",[i + 1 for i in range(num_pages)])
        return get_pages(0, num_pages,category_id,num_pages)
    else:
        # 正常页数分配
        # print("正常页数分配",[i + 1 for i in range(p - int(maxpage / 2), p + int(maxpage / 2))])
        return get_pages(p-1, p + maxpage-1 ,category_id,num_pages)


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

def get_media_download_infos_by_media_id(media_type,media_id):
    media=db.get_media_by_id(media_id)
    sections = db.get_media_sections_by_media_id(media_id)
    section_count = db.get_media_section_count_by_media_id(media_id)
    
    parent_dir = MEDIA_ROOT+media.ParentDir
    for link_key,link_val in link_map.items():
        if link_key in media.ParentDir:
            parent_dir = media.ParentDir.replace(link_key,link_val)
    file_path_list=[]
    zip_file_path=parent_dir+'/'+media.MediaName+'.zip'
    current_log.info(zip_file_path)
    if common_filer.exists(zip_file_path) and common_filer.get_file_size(zip_file_path) > 0:
        return zip_file_path
    else:
        for section in sections:
            real_file_path=parent_dir+'/'+media.MediaName+'_'+str(section.OrderNo)+'.'+section.Preffix
            if section_count == 1:
                real_file_path=parent_dir+'/'+media.MediaName+'.'+section.Preffix
            current_log.info(real_file_path)
            file_path_list.append(real_file_path)
        common_filer.add_files_into_zip(file_path_list, zip_file_path)
    return zip_file_path
    

def get_media_home_index(meida_type):
    return get_media_list(meida_type,category_map[meida_type][0].CategoryId,1)

def get_media_list(media_type,category_id,page_no):
    category_name = db.get_category_name_by_category_id(category_id)
    keys = ['media_type','source_list','contacts','pages','CategoryName']
    contacts = db.get_media_by_category_id(category_id, page_no, 30)
    total_count = db.get_media_count_by_category_id(category_id)
    max_page = total_count//30
    if total_count % 30 != 0:
        max_page = max_page+1
    pages = pages_help(page_no, max_page, category_id, 6)
    vals=[media_type,category_map[media_type],contacts,pages,category_name]
    return common_tools.create_map(keys, vals)

def get_media_content(media_type,media_id,order_no):
    media_section = db.get_media_section_by_media_id_order_no(media_id,order_no)
    media=db.get_media_by_id(media_id)
    total_count=db.get_media_section_count_by_media_id(media_id)
    category_name = db.get_category_name_by_category_id(media.CategoryId)
    comments=db.get_comments_by_category_key_and_item_id(media_type, media_section.Id)
    keys = ['media_type','source_list','media','media_section','total_count','CategoryName','comments']
    vals=[media_type,category_map[media_type],media,media_section,total_count,category_name,comments]
    return common_tools.create_map(keys, vals)

def init_common_book_info(link_dir,category):
    parent_dir = MEDIA_ROOT+link_dir
    for link_key,link_val in link_map.items():
        if link_key == link_dir:
            parent_dir = link_val
    current_dir = parent_dir+category.CategoryName+"/"
    if not common_filer.exists(current_dir):
        common_filer.make_dirs(current_dir)
    return current_dir

def get_blog_download_infos_by_article_id(article_id):
    article= db.get_article_by_id(article_id)
    article_name = article.Title
    category = db.get_category_by_id(article.CategoryId)[0]
    link_dir = "/blog/"
    current_dir=init_common_book_info(link_dir, category)
    file_path = current_dir + article_name + ".pdf"
    if common_filer.exists(file_path) and common_filer.get_file_size(file_path)>0:
        return file_path
    markdown_outputs = []
    try:
        markdown_reader = MarkDownReader(article.Content.replace("\r\n","\n"))
        markdown_tokens = markdown_reader.read_markdown()
        markdown_outputs=markdown_outputs+markdown_tokens
    except Exception as e:
        current_log.info(article_name)
        current_log.info(e)
    image_foler=link_map.get("/img/")
    pdfwriter.markdown_to_pdf(markdown_outputs,image_foler,"/media/img/",file_path)
    return file_path

def get_book_download_infos_by_book_id(book_type,book_id):
    book = db.get_book_by_id(book_id)
    book_name = book.BookName
    category = db.get_category_by_id(book.CategoryId)[0]
    book_sections=db.get_book_sections_by_book_id(book_id)
    link_dir = "/"+book_type+"/"
    current_dir=init_common_book_info(link_dir, category)
    if book_type == "novel":
        file_path = current_dir+book_name+".txt"
        if common_filer.exists(file_path) and common_filer.get_file_size(file_path)>0:
            return file_path
        file_w=SimpleFileWriter(file_path)
        file_w.append_new_line(book_name)
        file_w.append_new_line(book.Author)
        file_w.append_new_line(book.Description)
        for book_section in book_sections:
            file_w.append_new_line(book_section.ChapterName)
            file_w.append_new_line(book_section.Content)
        file_w.close()
        return file_path
    else:
        file_path = current_dir + book_name + ".pdf"
        if common_filer.exists(file_path) and common_filer.get_file_size(file_path)>0:
            return file_path
        markdown_outputs = []
        for book_section in book_sections:
            try:
                markdown_reader = MarkDownReader(book_section.Content.replace("\r\n","\n"))
                markdown_tokens = markdown_reader.read_markdown()
                markdown_outputs=markdown_outputs+markdown_tokens
            except Exception as e:
                current_log.info(book_section.ChapterName)
                current_log.info(e)
        image_foler=link_map.get("/img/")
        pdfwriter.markdown_to_pdf(markdown_outputs,image_foler,"/media/img/",file_path)
        return file_path

def get_book_home_index(book_type):
    return get_book_list(book_type,category_map[book_type][0].CategoryId,1)
    
def get_book_list(book_type,category_id,page_no):
    category_name = db.get_category_name_by_category_id(category_id)
    keys = ['book_type','source_list','contacts','pages','CategoryName']
    contacts = db.get_book_by_category_id(category_id, page_no, 20)
    total_count = db.get_book_count_by_category_id(category_id)
    max_page = total_count//20
    if total_count % 20 != 0:
        max_page = max_page+1
    pages = pages_help(page_no, max_page, category_id, 6)
    vals=[book_type,category_map[book_type],contacts,pages,category_name]
    return common_tools.create_map(keys, vals)

def get_book_info(book_type,book_id):
    keys=['book_type','source_list','book','CategoryName']
    book=db.get_book_by_id(book_id)
    category_name = db.get_category_name_by_category_id(book.CategoryId)
    vals=[book_type,category_map[book_type],book,category_name]
    return common_tools.create_map(keys, vals)

def get_book_menu_info(book_type,book_id):
    keys = ['book_type','source_list','book_menu_info','action','CategoryName']
    book_menu_info = db.get_booksections_by_id(book_id)
    category_name = db.get_category_name_by_category_id(book_menu_info.book.CategoryId)
    vals= [book_type,category_map[book_type],book_menu_info,'menu',category_name]
    return common_tools.create_map(keys, vals)

def get_book_section(section_id):
    return db.get_book_section_by_id(section_id)

def get_max_book_section_order_no(book_id):
    return db.get_max_book_section_order_no(book_id)

def get_book_section_info(book_type,book_id,section_order_no,max_section_order_no):
    keys = ['book_type','source_list','book_content_info','max_section_order_no','action','CategoryName','comments']
    book=db.get_book_by_id(book_id)
    book_content_info=db.get_book_content_include_prev_next_page(book_id,section_order_no, max_section_order_no)
    category_name = db.get_category_name_by_category_id(book.CategoryId)
    comments=db.get_comments_by_category_key_and_item_id(book_type, book_content_info.cur_content.Id)
    vals=[book_type,category_map[book_type],book_content_info,max_section_order_no,'section',category_name,comments]
    return common_tools.create_map(keys, vals)

def get_book_infos_by_author(book_type,book_id):
    book = db.get_book_by_id(book_id)
    author_name=book.Author
    keys = ['book_type','source_list','book_id','author_name','book_info_list','action']
    book_info_list = db.get_book_infos_by_author(author_name)
    vals = [book_type,category_map[book_type],book_id,author_name,book_info_list,'author']
    return common_tools.create_map(keys, vals)

def get_section_info(book_type,section_id):
    keys = ['book_type','source_list','section']
    section=db.get_book_section_by_id(section_id)
    vals=[book_type,category_map[book_type],section]
    return common_tools.create_map(keys, vals)

def get_book_section_by_order_no(book_id,order_no):
    return db.get_book_section_by_order_no(book_id,order_no)

def del_book_by_id(book_type,book_id):
    category_id=db.del_book_by_id(book_id)
    return get_book_list(book_type, category_id, 1)

def ins_book(book_dict):
    book_dict['MaxSectionId']=0
    return db.ins_book(book_dict)

def upd_book(book):
    db.upd_book(book)
    return book

def del_section_by_id(book_type,section_id):
    book_id=db.del_section_by_id(section_id)
    max_order_no=db.get_max_book_section_order_no(book_id)
    max_section = db.get_book_section_by_order_no(book_id, max_order_no)
    book=db.get_book_by_id(book_id)
    book.MaxSectionId=max_order_no
    book.MaxSectionName=get_maxsection_name(max_section)
    db.upd_book(book)
    return get_book_menu_info(book_type, book_id)

def get_maxsection_name(section):
    if section is not None:
        if section == '':
            return section
        return section.ChapterName
    return ''

def ins_section(section_dict):
    return db.ins_section(section_dict)

def upd_section(section):
    db.upd_section(section)
    return section

def get_blog_home_index():
    return get_blog_home_list(0, 1)

def get_blog_home_list(category_id,page_no):
    category_name='All'
    keys = ['category_list','article_list','contacts','hot_article_list','pages','CategoryName']
    if category_id == 0:
        article_list=db.get_articles_by_type()
    else:
        article_list=db.get_articles_by_category_id(category_id)
        category_name=db.get_category_name_by_category_id(category_id)
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
    vals=[blog_category_list,article_list,contacts,hot_article_list,pages,category_name]
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

def ins_comment_info(category_key,item_id,comment_content,user_id,user_name):
    return db.ins_comment_by_category_key_and_item_id(category_key, item_id, comment_content, user_id, user_name)

def del_comment_by_id(category_key,comment_id):
    return db.del_comment_by_id(category_key, comment_id)

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

# start not in use

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

def content_infos_to_text(content_infos):
    text_list=[]
    for content_info in content_infos:
        if content_info.ElementTag not in ['image','line']:
            text_str = content_info.Text.replace("BOLD[","").replace("]BOLD","").replace("BLUE_BG[","").replace("]BLUE_BG","")
            text_list.append(text_str)
    return "\n".join(text_list)

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

# end not in use