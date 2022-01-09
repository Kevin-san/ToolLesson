# -*-coding:utf-8-*-
'''
Created on 2019/6/10

@author: xcKev
'''
from alvintools import common_filer, common_threadpools
from alvinspider import common_spider
from alvinspider import SpiderContentItem, SpiderNovelItem
from concurrent.futures.thread import ThreadPoolExecutor
import time
from alvinspider.common_spider import current_log
from bs4.element import Tag
#https://www.23qb.net/
class NovelSpider():
    def __init__(self, url,index_attrs,content_attrs,home_path,category,name,spec_map=None):
        url_items = url.split('/')
        self.home_url = '/'.join(url_items[0:3])
        self.novel_url = url
        self.index_attrs = index_attrs.dict_attrs
        self.index_tag = index_attrs.tag
        self.content_attrs = content_attrs.dict_attrs
        self.content_tag = content_attrs.tag
        if spec_map and 'intro_attrs' in spec_map:
            intro_attrs = spec_map['intro_attrs']
            self.intro_tag = intro_attrs.tag
            self.intro_attrs = intro_attrs.dict_attrs
        if spec_map and 'author_attrs' in spec_map:
            author_attrs = spec_map['author_attrs']
            self.author_tag = author_attrs.tag
            self.author_attrs = author_attrs.dict_attrs
        if spec_map and 'image_attrs' in spec_map:
            image_attrs = spec_map['image_attrs']
            self.image_tag = image_attrs.tag
            self.image_attrs = image_attrs.dict_attrs
        self.name = name
        if name=='':
            self.name=url_items[-1]
        self.folder = common_filer.create_category_dir(home_path, category, name)
        self.thread_pool=ThreadPoolExecutor(1)
        self.thread_task_list=[]
        self.novel_dict=self.get_novel_dict_from_index_file()
        self.need_dl_dict=self.get_need_dl_dict()
    
    def get_need_dl_dict(self):
        need_dl_dict=dict()
        for title_name,spider_val in self.novel_dict.items():
            file_path=self.folder+'/'+title_name+'.txt'
            if common_filer.exists(file_path):
                if common_filer.get_file_size(file_path) ==0:
                    need_dl_dict[title_name]=spider_val
            else:
                need_dl_dict[title_name]=spider_val
        return need_dl_dict
    
    def get_novel_dict_from_index_file(self):
        novel_dict=dict()
        if common_filer.exists(self.folder+"/小说目录.txt"):
            novel_dict=common_filer.get_dict_from_file(self.folder+"/小说目录.txt")
        return novel_dict
    
    def execute_tasks(self,href_url,title_name,novels):
        common_threadpools.execute_thread_pool(self.thread_pool,self.thread_task_list, self.get_page_novel_title,href_url, title_name)
        for task_future in self.thread_task_list:
            if task_future.done():
                self.thread_task_list.remove(task_future)
                novels.append(task_future.result())
            if len(self.thread_task_list) > 10:
                time.sleep(30)

    def download(self, text_val, title_name):
        text_name = title_name + '.txt'
        cur_file = self.folder + '/' + text_name
        if common_filer.exists(cur_file) and common_filer.get_file_size(cur_file) >= len(text_val.encode("utf8")):
            current_log.info(F"{title_name} has been finished")
            return cur_file
        file_w = open(cur_file, 'w',encoding='utf-8')
        file_w.write(text_val)
        file_w.close()
        return cur_file
    
    def get_page_novel_title(self, url, title_name):
        text_val = self.get_page_novel_details(url)
        file_path=self.download(text_val, title_name)
        return SpiderNovelItem(title_name, url, text_val, file_path)
    
    def get_page_novel_detail(self, url):
        html = common_spider.get_response_text(url,'','',8)
        texts = common_spider.get_beautifulsoup_from_html(html, self.content_tag, attrs=self.content_attrs)
        detail_item = texts[0]
        return self.get_novel_text(detail_item)
    
    def get_page_novel_details(self,url):
        detail_text = self.get_page_novel_detail(url)
        if detail_text.find("（继续下一页）") !=-1:
            new_detail_text = self.get_page_novel_detail(url.replace(".html","_2.html"))
            return detail_text.replace("（继续下一页）", new_detail_text, 1)
        return detail_text
    
    def get_novel_text(self, html_tag):
        novel_text=""
        for novel_tag in html_tag.contents:
            if isinstance(novel_tag, Tag):
                if novel_tag.contents:
                    continue
                else:
                    novel_text+=novel_tag.text.replace('\xa0' * 8, '\n\n')
            else:
                novel_text+=novel_tag.string.replace('\xa0' * 8, '\n\n')
        return novel_text
    
    def write_index_dict(self,novel_list):
        file_w=open(self.folder+"/小说目录.txt","a+",encoding="utf8")
        for spider_item in novel_list:
            href_url=spider_item.spider_val
            title_name=spider_item.a_text
            file_w.write(F"{href_url} {title_name}\n")
        file_w.close()
    
    def get_page_novel_titles(self):
        html = common_spider.get_response_text(self.novel_url,'','',5)
        novels = []
        if self.index_attrs:
            div = common_spider.get_beautifulsoup_from_html(html, self.index_tag, attrs=self.index_attrs)
            a_list = common_spider.get_beautifulsoup_from_html(str(div[0]), 'a')
            for a_item in a_list:
                href_url = common_spider.get_correct_href(self.home_url, a_item)
                novels.append(SpiderContentItem('',a_item.text,href_url))
            return novels
        novels.append(SpiderContentItem('',self.name,self.novel_url))
        return novels
    
    def get_page_novel_author(self):
        html = common_spider.get_response_text(self.novel_url, '','',5)
        author_div = common_spider.get_beautifulsoup_from_html(html, self.author_tag, attrs=self.author_attrs)
        a_list = common_spider.get_beautifulsoup_from_html(str(author_div[0]), "a")
        a_item = a_list[0]
        return a_item.text

    def get_page_novel_intro(self):
        html = common_spider.get_response_text(self.novel_url, '','',5)
        intro_div = common_spider.get_beautifulsoup_from_html(html, self.intro_tag, attrs=self.intro_attrs)
        p_list = common_spider.get_beautifulsoup_from_html(str(intro_div[0]), "p")
        p_item = p_list[0]
        return p_item.text

    def get_page_novel_image(self):
        html = common_spider.get_response_text(self.novel_url, '','',5)
        image_div = common_spider.get_beautifulsoup_from_html(html, self.image_tag, attrs=self.image_attrs)
        img_list = common_spider.get_beautifulsoup_from_html(str(image_div[0]), "img")
        img_item = img_list[0]
        return img_item.get('src')
        
    def download_all_titles(self):
        novel_item_list=[]
        if self.novel_dict:
            if self.need_dl_dict:
                for title_name,spider_val in self.need_dl_dict.items():
                    self.execute_tasks(spider_val, title_name, novel_item_list)
                current_log.info(F"{self.name} missed some chapters")
                return novel_item_list
            current_log.info(F"{self.name} skipped")
            return novel_item_list
        novels = self.get_page_novel_titles()
        self.write_index_dict(novels)
        for spider_item in novels:
            current_log.info(spider_item.a_text)
            self.execute_tasks(spider_item.spider_val, spider_item.a_text, novel_item_list)
        current_log.info(F"{self.name} finished")
        return novel_item_list
    
    def download_to_one_novel(self):
        self.download_all_titles()
        whole_novel_text = ''
        title_names = []
        for title_name in self.get_novel_dict_from_index_file().keys():
            title_names.append(title_name)
            file_path=F"{self.folder}/{title_name}.txt"
            novel_detail = common_filer.get_file_detail(file_path)
            whole_novel_text += '\n\n' + title_name + '\n\n' + novel_detail
        file_path = self.download(whole_novel_text, self.name)
        return SpiderNovelItem(self.name, self.novel_url, '\n'.join(title_names), file_path)

