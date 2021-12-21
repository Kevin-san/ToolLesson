# -*-coding:utf-8-*-
'''
Created on 2021/7/24

@author: xcKev
'''
from spider import common_spider
from tools import common_tools
from spider import SpiderContentItem
from bs4.element import Tag
from spider.common_spider import current_log

class ParentSpider():
    def __init__(self, url, index_attrs, content_attrs,intro_attrs=None,author_attrs=None,image_attrs=None):
        url_items = url.split('/')
        self.home_url = '/'.join(url_items[0:3])
        self.group_url='/'.join(url_items[0:-1])
        self.url = url
        self.index_attrs = index_attrs.dict_attrs
        self.index_tag = index_attrs.tag
        self.content_attrs = content_attrs.dict_attrs
        self.content_tag = content_attrs.tag
        if author_attrs:
            self.author_tag = author_attrs.tag
            self.author_attrs = author_attrs.dict_attrs
        if intro_attrs:
            self.intro_tag = intro_attrs.tag
            self.intro_attrs = intro_attrs.dict_attrs
        if image_attrs:
            self.image_tag = image_attrs.tag
            self.image_attrs = image_attrs.dict_attrs
        self.target_html = common_spider.get_response_text(self.url,'','',0)
        self.index_m3u8_list=[]
        self.is_refered=True
        if index_attrs.index == 0:
            self.is_refered = False
    
    def get_page_titles(self):
        titles = []
        div = common_spider.get_beautifulsoup_from_html(self.target_html, self.index_tag, attrs=self.index_attrs)
        a_list = common_spider.get_beautifulsoup_from_html(str(div[-1]), 'a')
        for index,a_item in enumerate(a_list):
            href_url = common_spider.get_correct_href(self.home_url, a_item)
            titles.append(SpiderContentItem(index,a_item.text,href_url))
        return titles
    
    def get_html_text(self,current_url):
        if self.is_refered:
            return common_spider.get_response_text(current_url, '', '',0,self.home_url)
        else:
            return common_spider.get_response_text(current_url, '', '',0)
    
    def get_img_src(self,html):
        img_item=common_spider.get_beautifulsoup_from_html(html, 'img', {})
        img_org=img_item[0].get('data-original')
        img_src=img_item[0].get('src')
        img_url=img_item[0].get('url')
        if img_org is not None and img_org != img_src:
            return img_org
        if img_url is not None and img_url != img_src:
            return img_url
        return img_src

    def get_page_img_content(self,url,html):
        img_content_list=[]
        page_content=str(common_spider.get_beautifulsoup_from_html(html, self.content_tag, self.content_attrs)[0])
        page_items=common_spider.get_beautifulsoup_from_html(page_content, 'img', {})
        for img_item in page_items:
            img_src=self.get_img_src(str(img_item))
            img_content_list.append(SpiderContentItem(url,'',img_src))
        return img_content_list
    
    def get_page_img_index(self,current_url,img_list):
        html=self.get_html_text(current_url)
        img_list=img_list+self.get_page_img_content(current_url,html)
        if self.index_attrs:
            page_index=common_spider.get_beautifulsoup_from_html(html, self.index_tag, attrs=self.index_attrs)
            if page_index:
                page_bs4=common_spider.get_beautifulsoup_from_html(str(page_index[0]), 'a')
                return self.get_next_page_url(page_bs4,current_url,img_list)
        return '',img_list
    
    def get_next_page_url(self,page_bs4,current_url,img_list):
        for a_item in page_bs4:
            if str(a_item).find('下一页') !=-1 or str(a_item).find('下一张')!=-1:
                href_url=common_spider.get_correct_href(self.group_url, a_item)
                if href_url != current_url:
                    return href_url,img_list
        return '',img_list

    def get_page_img_indexs(self):
        href_url=self.url
        img_list=[]
        while href_url:
            href_url,img_list=self.get_page_img_index(href_url, img_list)
        return img_list
    
    def get_page_author(self):
        author_div = common_spider.get_beautifulsoup_from_html(self.target_html, self.author_tag, attrs=self.author_attrs)
        a_list = common_spider.get_beautifulsoup_from_html(str(author_div[0]), "a")
        if a_list:
            a_item = a_list[0]
            return a_item.text
        return 'alvin'
    
    def get_page_director(self):
        director_div = common_spider.get_beautifulsoup_from_html(self.target_html, self.author_tag, attrs=self.author_attrs)
        for director_div_text in director_div:
            a_list = common_spider.get_beautifulsoup_from_html(str(director_div_text), "a")
            if len(a_list) == 1:
                return a_list[0].text
        return 'alvin'
    
    def get_page_intro(self):
        intro_div = common_spider.get_beautifulsoup_from_html(self.target_html, self.intro_tag, attrs=self.intro_attrs)
        p_list = common_spider.get_beautifulsoup_from_html(str(intro_div[0]), "p")
        p_item = p_list[0]
        return p_item.text

    def get_page_image(self):
        image_div = common_spider.get_beautifulsoup_from_html(self.target_html, self.image_tag, attrs=self.image_attrs)
        img_list = common_spider.get_beautifulsoup_from_html(str(image_div[0]), "img")
        img_item = img_list[0]
        return common_spider.get_real_url(self.home_url, img_item.get('src'))
    
    def get_page_novel_detail(self, url):
        html = common_spider.get_response_text(url,'','',0)
        texts = common_spider.get_beautifulsoup_from_html(html, self.content_tag, attrs=self.content_attrs)
        detail_item = texts[0]
        return self.get_novel_text(detail_item)

    def get_novel_text(self, html_tag):
        novel_text=""
        for novel_tag in html_tag.contents:
            if isinstance(novel_tag, Tag):
                if novel_tag.contents:
                    if novel_tag.name != 'p':
                        continue
                    else:
                        text = novel_tag.text.replace('\xa0' * 8, '\n\n') + "\n"
                        novel_text+=text
                else:
                    novel_text+=novel_tag.text.replace('\xa0' * 8, '\n\n')
            else:
                novel_text+=novel_tag.string.replace('\xa0' * 8, '\n\n')
        return novel_text
    
    def get_video_index_srcs(self,index_m3u8):
        parent_url=index_m3u8.replace('/index.m3u8','',1)
        index_val=common_spider.get_response_text_with_no_encoding(index_m3u8, '', '', 0)
        return common_spider.parse_ts_list_from_m3u8(index_val, parent_url)
    
    def get_video_index_m3u8(self,script_text,index):
        index_m3u8=common_spider.get_javascript_index_m3u8(script_text)
        current_log.info(index_m3u8)
        if common_tools.is_list(index_m3u8):
            new_index_m3u8 = common_tools.get_filter_list_baseon_list(index_m3u8,self.index_m3u8_list)
            current_log.info(index)
            current_log.info(new_index_m3u8)
            if new_index_m3u8 and len(new_index_m3u8) <=2:
                self.index_m3u8_list.append(new_index_m3u8[0])
            else:
                self.index_m3u8_list=index_m3u8
            current_log.info(self.index_m3u8_list)
            return self.index_m3u8_list[index]
        else:
            return index_m3u8
        
    def get_video_real_index_m3u8(self,href_url,index):
        html=common_spider.get_response_text(href_url, '', '', 0)
        div=common_spider.get_beautifulsoup_from_html(html, self.content_tag, attrs=self.content_attrs)
        if self.index_m3u8_list and len(self.index_m3u8_list) > index:
            index_m3u8=self.index_m3u8_list[index]
            index_srcs = self.get_video_index_srcs(index_m3u8)
            return index_srcs[0]
        scripts=common_spider.get_beautifulsoup_from_html(str(div[0]), 'script')
        for script in scripts:
            script_text=common_spider.get_javascript_text(self.home_url,script)
            if script_text.find('/index.m3u8')!=-1:
                index_m3u8=self.get_video_index_m3u8(script_text,index)
                index_srcs = self.get_video_index_srcs(index_m3u8)
                return index_srcs[0]
        return ''