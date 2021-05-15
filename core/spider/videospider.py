#-*-coding:utf-8-*-
'''
Created on 2020/12/20

@author: xcKev
'''
from tools import common_filer, common_tools, common_threadpools
from spider import common_spider
from spider import SpiderContentItem,SpiderVideoItem
from concurrent.futures.thread import ThreadPoolExecutor
import time
from spider.common_spider import current_log
from spider import SpiderAttribute

class VideoSpider():
    def __init__(self,url,index_attrs,content_attrs,home_path,category,name):
        url_items=url.split('/')
        self.home_url='/'.join(url_items[0:3])+"/"
        self.video_url=url
        self.index_attrs = index_attrs.dict_attrs
        self.index_tag = index_attrs.tag
        self.content_attrs = content_attrs.dict_attrs
        self.content_tag = content_attrs.tag
        self.name=name
        self.index_m3u8_list=[]
        self.folder=common_filer.create_category_dir(home_path, category, name)
        self.summary_file=self.folder+'/'+self.name+'.txt'
        self.thread_pool=ThreadPoolExecutor(10)
        self.thread_task_list=[]
        
    def download_ts(self,video_src,episode_nm,cnt):
        common_filer.make_dirs(self.folder+'/'+episode_nm)
        video_name=episode_nm+'/'+str(cnt)+'.ts'
        cur_file=self.folder+'/'+video_name
        if common_filer.is_file(cur_file) and common_filer.get_file_size(cur_file)>0:
            return
        file_w=open(cur_file,'wb')
        current_log.info(video_src)
        response = common_spider.get_response(video_src, '', '')
        try:
            print(len(response.content))
            if response.content is not None and len(response.content) > 0:
                file_w.write(response.content)
            else:
                file_w.close()
                common_threadpools.execute_thread_pool(self.thread_pool,self.thread_task_list, self.download_ts,video_src,episode_nm,cnt)
        except:
            file_w.close()
            common_threadpools.execute_thread_pool(self.thread_pool,self.thread_task_list, self.download_ts,video_src,episode_nm,cnt)
        file_w.close()
    
    def download(self,key_map,video_srcs,episode_nm):
        cur_file=self.folder+'/'+episode_nm+'.ts'
        for index,video_src in enumerate(video_srcs):
            common_threadpools.execute_thread_pool(self.thread_pool, self.thread_task_list,self.download_ts,video_src,episode_nm,index)
            for task_future in self.thread_task_list:
                if task_future.done():
                    self.thread_task_list.remove(task_future)
            if len(self.thread_task_list) > 20:
                time.sleep(30)
        return common_filer.merge_ts_files(self.folder+'/'+episode_nm,key_map, cur_file)
    
    def get_video_real_index_m3u8(self,href_url,index):
        html=common_spider.get_response_text(href_url, '', '', 3)
        div=common_spider.get_beautifulsoup_from_html(html, self.content_tag, attrs=self.content_attrs)
        if self.index_m3u8_list and len(self.index_m3u8_list) > index:
            index_m3u8=self.index_m3u8_list[index]
            key_map, index_srcs = self.get_video_index_srcs(index_m3u8)
            return index_srcs[0]
        scripts=common_spider.get_beautifulsoup_from_html(str(div[0]), 'script')
        for script in scripts:
            script_text=common_spider.get_javascript_text(self.home_url,script)
            if script_text.find('/index.m3u8')!=-1:
                index_m3u8=self.get_video_index_m3u8(script_text,index)
                key_map, index_srcs = self.get_video_index_srcs(index_m3u8)
                return index_srcs[0]
        return ''
    
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
    
    def get_video_index_srcs(self,index_m3u8):
        index_srcs=[]
        parent_url=index_m3u8.replace('/index.m3u8','',1)
        index_val=common_spider.get_response_text_with_no_encoding(index_m3u8, '', '', 5)
        current_log.info(index_val)
        key_map=dict()
        is_dicon_cnt=0
        for line in index_val.split('\n'):
            if "#EXT-X-DISCONTINUITY" in line:
                is_dicon_cnt+=1
            if "#EXT-X-KEY" in line:
                method_pos = line.find("METHOD")
                comma_pos = line.find(",")
                method = line[method_pos:comma_pos].split('=')[1]
                uri_pos = line.find("URI")
                quotation_mark_pos = line.rfind('"')
                key_list=line[uri_pos:quotation_mark_pos].split('"')
                if len(key_list) == 2:
                    key_path = key_list[1]
                    key_url=common_spider.get_real_url(parent_url, key_path)
                    if not key_map:
                        res = common_spider.get_response(key_url, '', '')
                        key = res.content
                        key_map['key']=key
            if line is None or line =='' or line[0] == '#':
                continue
            http_url = common_spider.get_real_url(parent_url, line)
            if is_dicon_cnt%2 == 0:
                index_srcs.append(http_url)
        return key_map,index_srcs
    
    def get_page_video_episode(self,href_url,episode_name,index):
        index_m3u8 = self.get_video_real_index_m3u8(href_url,index)
        current_log.info(index_m3u8)
        return SpiderContentItem(href_url,episode_name,index_m3u8)
    
    def get_page_video_episodes(self):
        html=common_spider.get_response_text(self.video_url, '', '',3)
        if common_filer.is_file(self.summary_file) and common_filer.get_file_size(self.summary_file)> 10:
            return common_spider.get_spider_content_items(self.summary_file)    
        
        episodes=[]
        summary_file_h=open(self.summary_file,'w')
        if self.index_attrs:
            div = common_spider.get_beautifulsoup_from_html(html, self.index_tag, self.index_attrs)
            a_list=common_spider.get_beautifulsoup_from_html(str(div[0]), 'a')
            for index,a_item in enumerate(a_list):
                href_url=common_spider.get_correct_href(self.home_url, a_item)
                episode_nm="第"+str(index+1)+"集"
                if "" != a_item.text and a_item.text.find("集")!=-1:
                    episode_nm=a_item.text
                episode_item=self.get_page_video_episode(href_url, episode_nm,index)
                summary_file_h.write(F"{href_url} {episode_nm} {episode_item.spider_val}\n")
                episodes.append(episode_item)
            summary_file_h.close()
            return episodes
        episode_item=self.get_page_video_episode(self.video_url, self.name)
        summary_file_h.write(F"{self.video_url} {self.name} {episode_item.spider_val}\n")
        summary_file_h.close()
        episodes.append(episode_item)
        return episodes
    
    def download_all_videos(self):
        episodes=self.get_page_video_episodes()
        videos=[]
        for episode in episodes:
            href_url=episode.a_href
            episode_name=episode.a_text
            index_m3u8=episode.spider_val
            current_log.info(index_m3u8)
            if common_filer.is_file(self.folder+'/'+episode_name+'.mp4'):
                continue
            key_map,video_srcs=self.get_video_index_srcs(index_m3u8)
            index_file=open(self.folder+'/'+episode_name+'.txt','w')
            for id_key,video_src in enumerate(video_srcs):
                index_file.write(F"{video_src} {id_key}\n")
            index_file.close()
            file_path=self.download(key_map,video_srcs, episode_name)
            video_item=SpiderVideoItem(href_url,episode_name,file_path)
            videos.append(video_item)
        return videos
    
if __name__=="__main__":
#     videospider=VideoSpider("https://www.qmdy5.com/guochanju/jinxinsiyu/",SpiderAttribute(tag_name="div",id_v="",class_v="stui-pannel_bd col-pd clearfix"),SpiderAttribute(tag_name="div",id_v="",class_v="stui-pannel_bd col-pd clearfix"),"K:/Spider/video/","TV","锦心似玉")
    videospider=VideoSpider("https://www.qmdy5.com/guochanju/damingwangchao1566/",SpiderAttribute(tag_name="div",id_v="",class_v="stui-pannel_bd col-pd clearfix"),SpiderAttribute(tag_name="div",id_v="",class_v="stui-player__video clearfix"),"K:/Spider/video/","TV","大明王朝1566")
    videospider=VideoSpider("https://www.qmdy5.com/guochanju/changanshiershichen/",SpiderAttribute(tag_name="div",id_v="",class_v="stui-pannel_bd col-pd clearfix"),SpiderAttribute(tag_name="div",id_v="",class_v="stui-player__video clearfix"),"K:/Spider/video/","TV","长安十二时辰")
#     videospider=VideoSpider("https://www.qmdy5.com/guochanju/chenqingling/",SpiderAttribute(tag_name="div",id_v="",class_v="stui-pannel_bd col-pd clearfix"),SpiderAttribute(tag_name="div",id_v="",class_v="stui-player__video clearfix"),"K:/Spider/video/","TV","陈情令")
#     videospider=VideoSpider("http://www.qsptv.net/show-88092.html",{"class":"playlist"},{"id":"zanpiancms_player"},"F:/Python3/video/","TV","山海情")
    videospider.download_all_videos()