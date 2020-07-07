#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from PdfWeb.entitys import HomeIndexItem
from PdfWeb import db
from tools import common_tools


def get_group_list_key(detail_info):
    return '-'.join(detail_info.ParentKey.split('-')[0:3])

def get_group_str_key(detail_info):
    return detail_info.ParentKey

def get_home_index():
    menu_list = db.get_book_lesson_type_info()
    val_list = []
    for book_lesson_type in menu_list:
        index_list = db.get_book_lesson_image_info(book_lesson_type.Id)
        item = HomeIndexItem('index',book_lesson_type.CommonType,index_list)
        val_list.append(item)
    keys = ['menu_list','val_list']
    vals = [menu_list,val_list]
    return common_tools.create_map(keys,vals)

def get_chapter_headers(book_lesson_id):
    return db.get_chapter_infos(book_lesson_id)

def get_chapter_contents(chapter_id):
    return db.get_content_infos(chapter_id)
    
def get_chapters(book_lesson_id,chapter_href):
    header_list=get_chapter_headers(book_lesson_id)
    chapter_info=db.get_chapter_by_href(chapter_href)
    detail_list=get_chapter_contents(chapter_info.Id)
    content_html=convert_details_to_html(detail_list)
    keys = ['header_list','content_html']
    vals = [header_list,content_html]
    return common_tools.create_map(keys, vals)
        
def convert_details_to_html(detail_list):
    content_html=""
    rules1=['h2','p','pre','h1_span']
    rules2=['line']
"h1_span"
"line"
"p"
"h2"
"image"
"ul"
"table"
"blockquote"
"h3"
"pre"
"em"
"ol"
"h1"
"strong"
"h4"
"h5"
"a"


    for content_info in detail_list:
        tag = content_info.ElementTag
        text = content_info.Text
        dict = eval(content_info.AttributeMap)
    return ""


def convert_children_to_parent(children_details,check_cnt):
    if len(children_details) == check_cnt:
        return children_details
    val_dicts=common_tools.group_detail_by_dist_parent_key(common_tools.group_by_str, get_group_str_key, children_details)
    children_details.clear()
    for par_key,child_html in val_dicts.items():
        par_detail = db.get_parent_detail(par_key)
        detail_text = par_detail.Text
        par_detail.Text=common_tools.get_spec_var(detail_text, F"{child_html}", F"{par_detail.Text}{child_html}")
        children_details.append(par_detail)
    return convert_children_to_parent(children_details, check_cnt)

def get_complex_details(parent_key):
    typekey=F"{parent_key}"
    children_details=db.get_children_detail(typekey)
    child_details = db.get_child_details(parent_key)
    group_dicts = common_tools.group_detail_by_dist_parent_key(common_tools.group_by_list, get_group_list_key, children_details)
    children_details = convert_children_to_parent(children_details, len(group_dicts))
    child_details.extend(children_details)
    result_dicts = {}
    key_list = []
    for item in child_details:
        result_dicts[item.OrderIndex]=item.__str__()
        key_list.append(item.OrderIndex)
    sorted(key_list)
    return (key_list,result_dicts)

def convert_details_to_out_html(key_list,result_dicts):
    out_html=''
    for key_id in key_list:
        out_html=F"{out_html}{result_dicts[key_id]}"
    return out_html

def get_out_html(detail_info):
    tag = detail_info.Type
    t_class_str = F" class='{detail_info.ClassVal}'"
    t_id_str=F" id='{detail_info.IdVal}'"
    class_str=common_tools.get_spec_var(detail_info.ClassVal, "", t_class_str)
    id_str=common_tools.get_spec_var(detail_info.IdVal,"",t_id_str)
    class_id=F"{class_str}{id_str}"
    detail_text = common_tools.get_spec_var(detail_info.Text,"",detail_info.Text)
    if tag in ['hr','br']:
        return F"<{tag}>"
    if tag == 'img':
        img_info = db.get_image(detail_info.Text)
        return F'<{tag} src="{img_info.Src}" width="{img_info.Width}" height="{img_info.Height}" alt="{img_info.Alt}"{class_id}>'
    return F"<{tag}{class_id}>{detail_text}</{tag}>"