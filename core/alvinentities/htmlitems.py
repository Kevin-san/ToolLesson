#-*- encoding:UTF-8 -*-
'''
Created on 2019/12/28

@author: xcKev
'''

from bs4 import BeautifulSoup
from alvintools import common_tools

class SimpleHtmlItem():
    
    def __init__(self,from_type,tag_id,tag_name,tag_attrs,inner_text,html_flg):
        self.fr_type=from_type
        self.tag_idx=tag_id
        self.tag_name=tag_name
        self.attributes=tag_attrs
        self.text_str=inner_text
        self.html_flag=html_flg

    def __str__(self):
        return "fr_type:%s,tag_id:%s,name:%s,text:%s,flag:%s,attrs:%s" %(self.fr_type,self.tag_idx,self.tag_name,self.text_str,self.html_flag,str(self.attributes))
    
    def parse_values(self):
        inner_text=self.text_str
        if self.html_flag =="html":
            if inner_text.find("<img ")!=-1:
                self.tag_name="image"
                img = BeautifulSoup(inner_text,'lxml')
                img_tag = img.find('img')
                self.attributes=img_tag.attrs
                self.text_str = img_tag.attrs['src']
                self.html_flag = 'chtml'
            elif inner_text.find('<span class="color_h1">')!=-1:
                self.tag_name="h1_span"
                span = BeautifulSoup(inner_text,'lxml')
                span_tag = span.find('span')
                self.text_str = inner_text.replace(span_tag.prettify(),span_tag.string).replace("\n","")
                self.html_flag = 'chtml'
            elif self.tag_name == 'hr':
                self.tag_name = 'line'
                self.html_flag = 'chtml'
            elif common_tools.get_count(inner_text,'<strong>') >=1:
                self.text_str = inner_text.replace('<strong>','BOLD[').replace('</strong>',']BOLD')
                self.html_flag = 'chtml'
            elif common_tools.get_count(inner_text,'<span class="label label-info">') == common_tools.get_count(inner_text,'</span>'):
                self.text_str = inner_text.replace('<span class="label label-info">','BLUE_BG[').replace('</span>',']BLUE_BG')