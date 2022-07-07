# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
from alvinreadparser.filesreader import SimpleFileReader
from bs4 import BeautifulSoup
from alvinentities.htmlitems import SimpleHtmlItem
from alvintools import common_filer,common_converter,common_tools
from alvinwritecreater.fileswriter import SimpleFileWriter
import os
import base64
import quopri
from PdfWeb import current_log

class SimpleHtmlReader():
    
    def __init__(self,html_file):
        file_reader=SimpleFileReader(html_file)
        self.html_list=file_reader.read_lines()
        self.html_str="".join(self.html_list)
        
    def html2soup(self):
        return BeautifulSoup(self.html_str,'html5lib')
    
    def tosoup(self,html_text):
        return BeautifulSoup(html_text,'html5lib')
    
    def get_inner_html_text(self,html_tag):
        if html_tag.string is not None:
            inner_html = html_tag.string
        else:
            html_text = html_tag.prettify()
            tag_list = html_text.split("\n")[1:-2]
            inner_html="\n".join(tag_list)
        return self.correct_inner_html_str(html_tag.name,inner_html)
    
    def correct_inner_html_str(self,tag_name,inner_html):
        if tag_name == 'pre':
            return common_converter.htmlspec2str(inner_html)
        return common_converter.htmlspec2str(inner_html).replace("\n","")

    def get_inner_html_flag(self,html_tag):
        if html_tag.string is not None:
            return "text"
        else:
            return "html"

    def htmltags2list(self,root_tag,element_name):
        if root_tag.find_all(element_name):
            tag_string_list=[]
            for child_tag in root_tag.find_all(element_name):
                inner_html_text = self.get_inner_html_text(child_tag)
                if inner_html_text.find("<li>") !=-1:
                    htm_soup = self.tosoup(inner_html_text)
                    tab_tag = htm_soup.body
                    li_list = []
                    for ch_tag in tab_tag.find_all("li"):
                        li_list.append(ch_tag.string.strip().replace("\n",""))
                    parent_name = tab_tag.find("li").parent.name
                    inner_html_text = F"<{parent_name}>".join(li_list)
                tag_string_list.append(inner_html_text)
            return tag_string_list
        return []
    
    def tagslist2str(self,tag_string_list,split_char='\t'):
        return split_char.join(tag_string_list)
    
    def get_tablist_tagstr(self,child_tag):
        if child_tag.name in ['ul','ol']:
            grant_list=self.htmltags2list(child_tag,'li')
        elif child_tag.name == 'table':
            grant_list=[]
            for grant_tag in child_tag.find_all('tr'):
                if self.htmltags2list(grant_tag, 'th'):
                    grant_list.append(self.tagslist2str(self.htmltags2list(grant_tag, 'th'),'\t'))
                else:
                    grant_list.append(self.tagslist2str(self.htmltags2list(grant_tag, 'td'),'\t'))
        return self.tagslist2str(grant_list, '\n')
    
    def html2list(self,from_type):
        soup=self.html2soup()
        root_tag=soup.body
        self.item_list=[]
        index=1
        for child_tag in root_tag.find_all('div')[0].children:
            if child_tag.name is not None:
                if child_tag.name not in ['ul','ol','table']:
                    child_text=self.get_inner_html_text(child_tag)
                else:
                    child_text=self.get_tablist_tagstr(child_tag)
                html_flag=self.get_inner_html_flag(child_tag)
                item=SimpleHtmlItem(from_type,index,child_tag.name,child_tag.attrs,child_text,html_flag)
                item.parse_values()
                self.item_list.append(item)
                index=index+1
        return self.item_list
    
def get_child_files(correct_dir):
    map_dirs=dict()
    map_dirs['linux']=["index","install","plan","raidlvm","ipfirewalld","ssh","apache","vsftpd","sambanfs","bind","dhcp","postifxdevecot","squid","iscsi","mariadb","pxekickstart","lnmp","git","openstack","openldap"]
    map_dirs['bash']=["index","param","env","string","comment","argvs","escapechar","operator","array","hash","test","forever","func","output","include","vim","cmds"]
    return map_dirs[correct_dir]

def remove_django_pattern_parse_htm(directory,sub_dirs,suffix,replace_strs_dict):
    htm_dict={}
    for dirpath in sub_dirs:
        replace_strs=replace_strs_dict[dirpath]
        correct_dir=F"{directory}/{dirpath}"
        child_files=get_child_files(dirpath)
        htm_list=[]
        for child_file in child_files:
            child_file=F"{child_file}.html"
            if child_file in ["base.html","header.html"]:
                continue
            html_file=F"{correct_dir}/{child_file}"
            file_name=child_file.replace("html",suffix)
            htm_file=F"{correct_dir}/{file_name}"
            file_wrter=SimpleFileWriter(htm_file,'w+')
            file_rder=SimpleFileReader(html_file)
            line_list=file_rder.read_lines()
            new_line_list=[]
            for line in line_list:
                if line not in replace_strs:
                    new_line_list.append(line)
            file_wrter.append_lines(new_line_list)
            htm_list.append(htm_file)
            file_rder.close()
            file_wrter.close()
        htm_dict[dirpath]=common_tools.to_unique_list(htm_list)
    return htm_dict

def clear_htm_files(corr_dir):
    for child_file in common_filer.get_child_files(corr_dir):
        if child_file.endswith(".htm") and os.path.exists(child_file):
            os.remove(F"{corr_dir}/{child_file}")

def get_rpl_strs(corr_dir):
    return ['{% extends "'+corr_dir+'/base.html" %}','{% block content %}','{% endblock %}']
              
def get_replace_strs(rpl_strs):
    replace_strs=[]
    for rpl_str in rpl_strs:
        replace_strs.append(rpl_str)
        replace_strs.append(rpl_str+'\n')
        replace_strs.append(rpl_str+'\r\n')
        replace_strs.append(rpl_str+'\R')
    return replace_strs
    
def parse_htm_list_to_sql(htm_dict,chapter_sql,content_sql):
    index_no=1
    content_id=1
    chapter_sql_wrter=SimpleFileWriter(chapter_sql)
    content_sql_wrter=SimpleFileWriter(content_sql)
    chapter_sql_wrter.append_new_line("delete from Chapter;")
    content_sql_wrter.append_new_line("delete from Content;")
    for directory_path,htm_list in htm_dict.items():
        for chapter_id,htm_file in enumerate(htm_list):
            htm_rder=SimpleHtmlReader(htm_file)
            file_name=os.path.basename(htm_file).replace(".htm","")
            chapter_no=chapter_id+1
            href=F"{directory_path}/{file_name}"
            item_list=htm_rder.html2list(href)
            chapter_data_sql=F"insert into Chapter values({index_no},'{directory_path}',{chapter_no},'{file_name}','{href}',0,'alvin',curdate());"
            chapter_sql_wrter.append_new_line(chapter_data_sql)
            for item in item_list:
                tag_name=item.tag_name
                tag_id=item.tag_idx
                attrs=str(item.attributes).replace("'",'"')
                text=item.text_str.replace("'","\\'")
                content_data_sql=F"insert into Content values({content_id},{index_no},'{tag_name}',{tag_id},'{attrs}','{text}','{text}',0,'alvin',sysdate());"
                content_sql_wrter.append_new_line(content_data_sql)
                content_id=content_id+1
            index_no=index_no+1

def convert_mht_to_list(boundary, html_content):
    return str(html_content).split(boundary)

def get_boundary(html_lines):
    for line in html_lines:
        if "".join(line.split()).startswith("boundary="):
            boundary="--"+str(line).split('boundary=')[-1].replace('"',"")
            current_log.info(boundary)
            return boundary

def save_image_file(image_content, folder, file_name):
    try:
        file_path = os.path.join(folder, file_name)
        current_log.info(folder)
        common_filer.make_dirs(folder)
        f= open(file_path, 'wb')
        f.write(image_content)
        current_log.info('%s 保存图片成功' %(file_path))
        return file_path
    except Exception as e:
        # print(e)
        current_log.info('%s 保存图片失败: ' %( str(e)))
        return None

def get_content_val(content_key,content_line):
    current_log.info(content_key)
    content_val =content_line.split(content_key+":")[1].strip()
    return content_val

def get_content_val_from_sub_content(content_key,sub_content):
    content_val = 'unknown'
    for sub_line in sub_content:
        if content_key in sub_line:
            return get_content_val(content_key, sub_line)
    return content_val

def get_content_type(sub_content):
    return get_content_val_from_sub_content('Content-Type',sub_content)

def get_content_location(sub_content):
    return get_content_val_from_sub_content('Content-Location',sub_content)

def get_content_encoding(sub_content):
    return get_content_val_from_sub_content('Content-Transfer-Encoding',sub_content)

def get_img_content(sub_content):
    begin_index = 0
    content_keys = ['Content-Type','Content-Transfer-Encoding','Content-Location']
    for sub_index,sub_line in enumerate(sub_content):
        for content_key in content_keys:
            if content_key in sub_line:
                begin_index = sub_index+1
    return ''.join(sub_content[begin_index:])

def get_content_type_and_content(line, sub_path_name, file_name):
    line = str(line)
    sub_content = line.split('\n')
    if 'Content-Location' in line:
        content_type = get_content_type(sub_content)
        content_encoding= get_content_encoding(sub_content)
        content = get_img_content(sub_content)
        if 'image' in content_type:
            current_log.info('正在保存图片文件:%s ' % (file_name))
            decoded_body = None
            if content_encoding.lower() == 'quoted-printable':
                decoded_body = quopri.decodestring(content)
            if content_encoding.lower() == 'base64':
                try:
                    decoded_body = base64.b64decode(content)
                except Exception:
                    current_log.info('%s 图片解码失败，无法保存' %(file_name))
                    return
            if decoded_body:
                save_image_file(decoded_body, sub_path_name, file_name)
        else:
            current_log.info('%s 图片解码失败，无法保存')

def save_mht_all_images(input_path):
    parent_folder = common_filer.get_parent_dir(input_path)
    file_name_full = common_filer.get_file_name(input_path)
    file_key = file_name_full.replace(".mht","")
    current_log.info(file_key)
    sub_path_name = os.path.join(parent_folder, file_key)
    file_reader= SimpleFileReader(input_path)
    all_lines = file_reader.read_lines()
    file_reader2=SimpleFileReader(input_path)
    body_content = file_reader2.read()
    boundary = get_boundary(all_lines)
    content_list = convert_mht_to_list(boundary, html_content=body_content)
    index = 1
    for content_l in content_list:
        sub_content = content_l.split('\n')
        content_type = get_content_type(sub_content)
        if "image" in content_type:
            file_name = file_key+"_"+str(index)+".jpg"
            get_content_type_and_content(content_l, sub_path_name, file_name)
            index += 1
        else:
            continue
    file_reader.close()
    
def save_mhts_all_images(input_path_map,parent_dir):
    for input_key, vals in input_path_map.items():
        sub_path_name = os.path.join(parent_dir, input_key)
        index = 0
        for input_val in vals:
            current_log.info(input_val)
            input_path = parent_dir + input_val
            file_reader= SimpleFileReader(input_path)
            all_lines = file_reader.read_lines()
            file_reader2=SimpleFileReader(input_path)
            body_content = file_reader2.read()
            boundary = get_boundary(all_lines)
            content_list = convert_mht_to_list(boundary, html_content=body_content)
            for content_l in content_list:
                sub_content = content_l.split('\n')
                content_type = get_content_type(sub_content)
                current_log.info(content_type)
                if "image" in content_type:
                    file_name = input_key+"_"+str(index)+".jpg"
                    get_content_type_and_content(content_l, sub_path_name, file_name)
                    index += 1
                else:
                    continue
            file_reader.close()
            file_reader2.close()
if __name__ == "__main__":
    parent_path = "Y:/Spider/Hider/Image/漫画"
    input_path_map={'[DISTANCE]淫女桃花运！_じょしラク！ [彩图整合][风与Y⑨] [245p]':['/unzip/[DISTANCE]淫女桃花运！_じょしラク！ [彩图整合][风与Y⑨] [245p].mht'],
'[MGMEE] 女子宅宅圈里的王子殿下☆ _女子オタサーの王子様☆ [风的工房] [195p]':['/unzip/[MGMEE] 女子宅宅圈里的王子殿下☆ _女子オタサーの王子様☆ [风的工房] [195p].mht'],
'[TANA][キミの瞳に欲情[コイ]してる 初回限定版] [219p]':['/unzip/[TANA][キミの瞳に欲情[コイ]してる 初回限定版] [219p].mht'],
'[ごばん] 一求乳魂 [开坑当做例行重嵌组][高画质] [238p]':['/unzip/[ごばん] 一求乳魂 [开坑当做例行重嵌组][高画质] [238p].mht'],
'[サブロー] 艶肌らう゛ぁーず [全彩][风与彧与uuz与ahei与风雷与嘘与龙爷与ハル与小红与蜡笔与丧尸汉化] [117p]':['/unzip/[サブロー] 艶肌らう゛ぁーず [全彩][风与彧与uuz与ahei与风雷与嘘与龙爷与ハル与小红与蜡笔与丧尸汉化] [117p].mht'],
'[しいなかずき]魔界植物ギジエール先生 [188p]':['/unzip/[しいなかずき]魔界植物ギジエール先生 [188p].mht'],
'[ふぁんとむ] 生插入膣射出洗脑中_生ハメ膣出し洗脳中 [风与Y⑨製作] [177p]':['/unzip/[ふぁんとむ] 生插入膣射出洗脑中_生ハメ膣出し洗脳中 [风与Y⑨製作] [177p].mht'],
'[皐月芋网] 都市传说淫女妖-女子怪-_都市伝説ビッチ-女子怪- [风的工房] [177p]':['/unzip/[皐月芋网] 都市传说淫女妖-女子怪-_都市伝説ビッチ-女子怪- [风的工房] [177p].mht'],
'[松本ドリル研究所] まマまま！ [249p]':['/unzip/[松本ドリル研究所] まマまま！ [249p].mht'],
'[真秀] ちょきっとデュラハン! [妖魔女孩们也都很好色! [175p]':['/unzip/[真秀] ちょきっとデュラハン! [妖魔女孩们也都很好色! [175p].mht']
}
    save_mhts_all_images(input_path_map, parent_path)