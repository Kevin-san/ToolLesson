#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/10

@author: xcKev
'''
from alvintools import common_filer,common_threadpools
from alvinspider import common_spider
from concurrent.futures.thread import ThreadPoolExecutor
import time
from alvinspider import SpiderContentItem,SpiderImgItem
from alvinspider.common_spider import current_log

class ImgSpider():
    def __init__(self,url,index_attrs,content_attrs,home_path,category,name):
        url_items=url.split('/')
        url_vals=url_items[2].split('.')
        self.home_url='/'.join(url_items[0:3])
        self.group_url='/'.join(url_items[0:-1])
        self.img_url=url
        self.index_attrs=index_attrs.dict_attrs
        self.index_tag=index_attrs.tag
        self.content_attrs=content_attrs.dict_attrs
        self.content_tag=content_attrs.tag
        self.name=name
        self.is_refered=True
        if index_attrs.index == 0:
            self.is_refered = False
        self.thread_pool=ThreadPoolExecutor(20)
        self.thread_task_list=[]
        if name=='':
            self.name=url_items[-1]
        self.folder=home_path+'/'+category+'/'+url_vals[1]+'/'+self.name
        common_filer.make_dirs(self.folder)
        self.img_dict=self.get_img_dict_from_map_dict()
        self.need_dl_dict=self.get_need_dl_dict()
    
    def get_need_dl_dict(self):
        need_dl_dict=dict()
        for img_index,spider_val in self.img_dict.items():
            file_path=self.folder+'/'+self.name+'_'+img_index+'.'+spider_val.split('/')[-1].split('.')[-1]
            if common_filer.exists(file_path):
                if common_filer.get_file_size(file_path) ==0:
                    need_dl_dict[img_index]=spider_val
            else:
                need_dl_dict[img_index]=spider_val
        return need_dl_dict
    
    def get_img_dict_from_map_dict(self):
        img_dict=dict()
        if common_filer.exists(self.folder+"/映射.txt"):
            img_dict=common_filer.get_dict_from_file(self.folder+"/映射.txt")
        return img_dict
    
    
    def execute_tasks(self,spider_item,img_index,imgs):
        common_threadpools.execute_thread_pool(self.thread_pool,self.thread_task_list, self.get_img_item,img_index,spider_item)
        for task_future in self.thread_task_list:
            if task_future.done():
                self.thread_task_list.remove(task_future)
                imgs.append(task_future.result())
            if len(self.thread_task_list) > 10:
                time.sleep(30)

    def download(self,img_src,cnt):
        img_name=self.name+'_'+str(cnt)+'.'+img_src.split('/')[-1].split('.')[-1]
        if self.is_refered:
            res=common_spider.get_response_by_seconds(img_src, '','',5,self.home_url)
        else:
            res= common_spider.get_response_by_seconds(img_src, '','',5)
        cur_file=self.folder+'/'+img_name
        file_w=open(cur_file,'wb')
        file_w.write(res.content)
        file_w.close()
        return cur_file
    
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
    
    def get_html_text(self,current_url):
        if self.is_refered:
            return common_spider.get_response_text(current_url, '', '',3,self.home_url)
        else:
            return common_spider.get_response_text(current_url, '', '',3)
    
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
        href_url=self.img_url
        img_list=[]
        while href_url:
            href_url,img_list=self.get_page_img_index(href_url, img_list)
        return img_list
    
    def get_page_img_content(self,url,html):
        img_content_list=[]
        page_content=str(common_spider.get_beautifulsoup_from_html(html, self.content_tag, self.content_attrs)[0])
        page_items=common_spider.get_beautifulsoup_from_html(page_content, 'img', {})
        for img_item in page_items:
            img_src=self.get_img_src(str(img_item))
            img_content_list.append(SpiderContentItem(url,'',img_src))
        return img_content_list
    
    def get_img_item(self,index,spider_item):
        img_src=spider_item.spider_val
        file_path=self.download(img_src, index)
        img_item=SpiderImgItem(spider_item.a_href,img_src,file_path)
        return img_item
    
    def write_map_dict(self,img_list):
        file_w=open(self.folder+"/映射.txt","a+")
        for index,spider_item in enumerate(img_list):
            img_src=spider_item.spider_val
            file_w.write(F"{img_src} {index}\n")
        file_w.close()
    
    def download_all_imgs(self):
        img_item_list=[]
        if self.img_dict:
            if self.need_dl_dict:
                for index,spider_val in self.need_dl_dict.items():
                    spider_item=SpiderContentItem(self.home_url,'',spider_val)
                    self.execute_tasks(spider_item, index, img_item_list)
                current_log.info(F"{self.name} missed some pictures")
                return img_item_list
            current_log.info(F"{self.name} skipped")
            return img_item_list
        img_list=self.get_page_img_indexs()
        self.write_map_dict(img_list)
        for index,spider_item in enumerate(img_list):
            self.execute_tasks(spider_item, index, img_item_list)
        current_log.info(F"{self.name} finished")
        return img_item_list
