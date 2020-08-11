#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from PdfWeb.entitys import HomeIndexItem
from PdfWeb import db,entitys
from tools import common_tools, common_converter

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
    chapter_infos=db.get_chapter_by_href(chapter_href)
    chapter_info=chapter_infos[0]
    detail_list=get_chapter_contents(chapter_info.Id)
    content_html=convert_details_to_html(detail_list)
    keys = ['header_list','content_html']
    vals = [header_list,content_html]
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
