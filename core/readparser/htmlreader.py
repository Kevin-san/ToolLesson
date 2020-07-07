# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
from readparser.filesreader import SimpleFileReader
from bs4 import BeautifulSoup
from entitys.htmlitems import SimpleHtmlItem
from tools import common_filer,common_converter,common_tools
from writecreater.fileswriter import SimpleFileWriter
import os

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
            chapter_data_sql=F"insert into Chapter values({index_no},'{directory_path}',{chapter_no},'{file_name}','{href}',0,'alvin',sysdate());"
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
if __name__ == "__main__":
    directory="C:/Users/xcKev/git/CorePdfPage/templates"
    sql_dir="C:/Users/xcKev/git/CorePdfPage/sql/mysql/correct_table"
    chapter_sql_file=F"{sql_dir}/ChapterData1.sql"
    content_sql_file=F"{sql_dir}/ContentData1.sql"
    dirs=["linux","bash"]
    replace_strs_dict={}
    for corr_dir in dirs:
        clear_htm_files(F"{directory}/{corr_dir}")
        rpl_strs=get_rpl_strs(corr_dir)
        replace_strs=get_replace_strs(rpl_strs)
        replace_strs_dict[corr_dir]=replace_strs
    htm_dict=remove_django_pattern_parse_htm(directory, dirs, 'htm', replace_strs_dict)
    parse_htm_list_to_sql(htm_dict,chapter_sql_file,content_sql_file)