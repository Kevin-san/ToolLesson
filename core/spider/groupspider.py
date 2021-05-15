#-*-coding:utf-8-*-
'''
Created on 2021/1/4

@author: xcKev
'''
from tools import common_filer, common_threadpools
from spider import common_spider, novelspider
from spider import GroupAttribute,SpiderAttribute,SpiderParameters
from spider.imgspider import ImgSpider
from retrying import retry
from spider.common_spider import current_log
from spider.novelspider import NovelSpider
from spider.videospider import VideoSpider
import random
import time

def get_group_attributes(list_attrs):
    group_attr_dicts=dict()
    for attr_key,attr_dict in list_attrs.items():
        block_spider_attr=GroupAttribute.get_block_spider_attribute(attr_dict)
        item_spider_attr=GroupAttribute.get_item_spider_attribute(attr_dict)
        children_spider_attr=GroupAttribute.get_children_spider_attribute(attr_dict)
        page_spider_attr=GroupAttribute.get_page_spider_attribute(attr_dict)
        group_attr_dicts[attr_key]=GroupAttribute(block_spider_attr,item_spider_attr,children_spider_attr,page_spider_attr)
    return group_attr_dicts

group_attrs={
    "http://www.paoshuzw.com/":{"block_tag":"div","block_class":"l","block_id":"","item_tag":"li","item_class":"","item_id":"","children_tag":"a","children_index":"1","children_href":"a.href","children_text":"a.text","page_tag":"a","page_class":"next","page_id":""},
    "http://www.quanji456.com":{"block_tag":"div","block_class":"classpage","block_id":"","item_tag":"li","item_class":"","item_id":"","children_tag":"a","children_index":"1","children_href":"a.href","children_text":"a.text","page_tag":"","page_class":"","page_id":""},
    "https://www.qiqidongman.com/":{"block_tag":"ul","block_class":"ulPic fix","block_id":"LIST","item_tag":"li","item_class":"","item_id":"","children_tag":"a","children_index":"1","children_href":"a.href","children_text":"a.title","page_tag":"div","page_class":"pages r","page_id":""},
    "http://www.mm288.com/":{"block_tag":"div","block_class":"","block_id":"infinite_scroll","item_tag":"div","item_class":"ABox","item_id":"","children_tag":"a","children_index":"1","children_href":"a.href","children_text":"img.alt","page_tag":"div","page_class":"NewPages","page_id":""},
    "http://www.mm4000.com/meinv/":{"block_tag":"ul","block_class":"l-meinv-wrapp cl","block_id":"","item_tag":"div","item_class":"timg","item_id":"","children_tag":"a","children_index":"1","children_href":"a.href","children_text":"img.alt","page_tag":"div","page_class":"pagelists","page_id":""},
    "https://www.ku66.net/":{"block_tag":"div","block_class":"TypeList","block_id":"","item_tag":"li","item_class":"","item_id":"","children_tag":"a","children_index":"1","children_href":"a.href","children_text":"div.innerHtml","page_tag":"div","page_class":"NewPages","page_id":""},
    "https://www.mzitu.com/":{"block_tag":"ul","block_class":"","block_id":"pins","item_tag":"li","item_class":"","item_id":"","children_tag":"a","children_index":"1","children_href":"a.href","children_text":"img.alt","page_tag":"a","page_class":"next page-numbers","page_id":""},
}
detail_attrs={
    "picture":{
#         "http://www.mm288.com/":{
#             "index_attrs":SpiderAttribute(tag_name="ul",id_v="mouse_page",class_v="articleV2Page",index=0),
#             "content_attrs":SpiderAttribute(tag_name="div",id_v="big-pic",class_v="")
#         },
        "https://www.ku66.net/":{
            "index_attrs":SpiderAttribute(tag_name="div",id_v="",class_v="NewPages"),
            "content_attrs":SpiderAttribute(tag_name="div",id_v="",class_v="content")
        },
        "http://www.mm4000.com/":{
            "index_attrs":SpiderAttribute(tag_name="div",id_v="pageNum",class_v=""),
            "content_attrs":SpiderAttribute(tag_name="li",id_v="showimages",class_v="")
        },
        "https://www.mzitu.com/":{
            "index_attrs":SpiderAttribute(tag_name="div",id_v="",class_v="pagenavi"),
            "content_attrs":SpiderAttribute(tag_name="div",id_v="",class_v="main-image")
        }
    },
    "novel":{
        "http://www.paoshuzw.com/":{
            "index_attrs":SpiderAttribute(tag_name="div",id_v="list",class_v="",index=0),
            "content_attrs":SpiderAttribute(tag_name="div",id_v="content",class_v="")
        }
    },
    "video":{
#         "http://www.quanji456.com/":{
#             "index_attrs":SpiderAttribute(tag_name="div",id_v="jishu",class_v=""),
#             "content_attrs":SpiderAttribute(tag_name="div",id_v="",class_v="commendType")
#         },
#         quanji456 : qvod:// aaa|aaa|xxx.rmvb  , mp4 , index.m3u8
#         "https://www.qiqidongman.com/":{
#             "index_attrs":SpiderAttribute(tag_name="div",id_v="",class_v="tb fix"),
#             "content_attrs":SpiderAttribute(tag_name="div",id_v="",class_v="playBox")
#         }
#         qiqidongman: iframe : src = *.mp4
#         电影天堂尝试爬取
    }
}

group_map_attrs=get_group_attributes(group_attrs)
dict_attrs={
    "novel":[
"http://www.paoshuzw.com/xuanhuanxiaoshuo/",
"http://www.paoshuzw.com/xiuzhenxiaoshuo/",
"http://www.paoshuzw.com/dushixiaoshuo/",
"http://www.paoshuzw.com/chuanyuexiaoshuo/",
"http://www.paoshuzw.com/wangyouxiaoshuo/",
"http://www.paoshuzw.com/kehuanxiaoshuo/",
"http://www.paoshuzw.com/xiaoshuodaquan/",],
    "video":[
"http://www.quanji456.com/Zuixindaluju/",
"http://www.quanji456.com/Zuixinmeiju/",
"http://www.quanji456.com/Zuixinhanju/",
"http://www.quanji456.com/Zuixintaiju/",
"http://www.quanji456.com/Zuixinriju/",
"http://www.quanji456.com/Zuixingangju/",
"http://www.quanji456.com/Taiguodianshiju/",
"http://www.quanji456.com/Dongzuodianying/",
"http://www.quanji456.com/Xijudianying/",
"http://www.quanji456.com/Aiqingdianying/",
"http://www.quanji456.com/Kehuandianying/",
"http://www.quanji456.com/Kongbudianying/",
"http://www.quanji456.com/Zhanzhengdianying/",
"http://www.quanji456.com/Juqingdianying/",
"http://www.quanji456.com/Dongman/",
"http://www.quanji456.com/Zuixinzongyi/",
"https://www.qiqidongman.com/vod-search.html"
],
"picture":[

"http://www.mm288.com/meinv/",
"http://www.mm288.com/meinv/xgcm/",
"http://www.mm288.com/meinv/mnxh/",
"http://www.mm288.com/meinv/mnmt/",
"http://www.mm288.com/meinv/jpmn/",
"http://www.mm288.com/meinv/mnzp/",
"http://www.mm288.com/meinv/rtys/",
"http://www.mm288.com/meinv/gzmn/",
"http://www.mm288.com/meinv/wgmn/",
"http://www.mm288.com/meinv/hgmn/",
"http://www.mm288.com/meinv/rbmn/",
"http://www.mm288.com/meinv/ommn/",
"http://www.mm288.com/meinv/zfyh/",
"http://www.mm288.com/mvtp/zgmn/",
"http://www.mm288.com/mvtp/rhmn/",
"http://www.mm288.com/mvtp/ommn/",
"http://www.mm288.com/mvtp/dlmn/",
"http://www.mm288.com/mvtp/rbmn/",
"http://www.mm288.com/mvtp/hgmn/",
"http://www.mm288.com/mvtp/twmn/",
"http://www.mm288.com/xgmn/",
"http://www.mm288.com/qcmn/",
"http://www.mm288.com/mnxz/",
"http://www.mm288.com/swmt/",
"http://www.mm288.com/mxmn/",
"http://www.mm288.com/mnbz/",
"http://www.mm288.com/dmmn/",
"http://www.mm288.com/dmmn/cosplay/",
"http://www.mm4000.com/meinv/",
"https://www.ku66.net/r/1/index.html",
"https://www.mzitu.com/"
    ]
}


    
# novel
# index : div(id/class) : ul -> li ( no.1 a tag )| next_page : div(id/class)   http://www.paoshuzw.com/
# block_tag=div,block_class=l,block_id=,item_tag=li,item_class=,children_tag=a,children_index=1,children_href=a.href,children_text=a.text,page_tag=a,page_class=next,page_key=下一页  
# music
# index : single ul(id/class) -> li ( no.1 a tag ) no next_page http://www.yue365.com/
# index : duplicate ul(id/class) -> li ( no.1 a tag ) no next_page http://www.5nd.com/
# index : duplicate div(id/class) -> li ( no.1 a tag ) no next_page https://www.9ku.com/
# index : single ul(id/class) -> li ( no.1 a tag )| next_page : div(id/class) http://www.htqyy.com/
# video :
# index : duplicate div(id/class) -> li ( no.1 a tag ) | no next_page http://www.quanji456.com/
# http://www.quanji456.com/Zuixindaluju/
# http://www.quanji456.com/Zuixinmeiju/
# http://www.quanji456.com/Zuixinhanju/
# http://www.quanji456.com/Zuixintaiju/
# http://www.quanji456.com/Zuixinriju/
# http://www.quanji456.com/Zuixingangju/
# http://www.quanji456.com/Taiguodianshiju/
# http://www.quanji456.com/Dongzuodianying/
# http://www.quanji456.com/Xijudianying/
# http://www.quanji456.com/Aiqingdianying/
# http://www.quanji456.com/Kehuandianying/
# http://www.quanji456.com/Kongbudianying/
# http://www.quanji456.com/Zhanzhengdianying/
# http://www.quanji456.com/Juqingdianying/
# http://www.quanji456.com/Dongman/
# http://www.quanji456.com/Zuixinzongyi/
# block_tag=div,block_class=classpage,item_tag=li,item_class=,children_tag=a,children_index=1,children_href=a.href,children_text=a.text,page_tag=,page_class=,page_key=
# index : single ul(id/class) -> li ( no.1 a tag )| next_page : div(id/class) https://www.qiqidongman.com/
# block_tag=ul,block_class=ulPic fix,block_id=LIST,item_tag=li,item_class=,children_tag=a,children_index=1,children_href=a.href,children_text=a.text,page_tag=a,page_class=pagebk,page_key=下一页
# image
# index : single div(id/class) -> ( no.1 a tag )| next_page : div(id/class)   http://www.mm288.com/
# http://www.mm288.com/meinv/  index dup_parents:tag=div,class=ABox, children:href=a.href,text=img.alt  || page tag=div,class=NewPages,next_page.id=下一页
# http://www.mm288.com/meinv/xgcm/ index dup_parents:block_tag=div,id=infinite_scroll,item_tag=div,class=ABox, children_tag=a,children_index=1,href=a.href,text=img.alt  || page_tag=div,class=NewPages,next_page.id=下一页
# http://www.mm288.com/meinv/mnxh/ block_tag=div,block_id=infinite_scroll,item_tag=div,item_class=ABox,children_tag=a,children_index=1,children_href=a.href,children_text=img.alt,page_tag=div,page_class=NewPages,page_key=下一页
# http://www.mm288.com/meinv/mnmt/
# http://www.mm288.com/meinv/jpmn/
# http://www.mm288.com/meinv/mnzp/
# http://www.mm288.com/meinv/rtys/
# http://www.mm288.com/meinv/gzmn/
# http://www.mm288.com/meinv/wgmn/
# http://www.mm288.com/meinv/hgmn/
# http://www.mm288.com/meinv/rbmn/
# http://www.mm288.com/meinv/ommn/
# http://www.mm288.com/meinv/zfyh/
# http://www.mm288.com/mvtp/zgmn/
# http://www.mm288.com/mvtp/rhmn/
# http://www.mm288.com/mvtp/ommn/
# http://www.mm288.com/mvtp/dlmn/
# http://www.mm288.com/mvtp/rbmn/
# http://www.mm288.com/mvtp/hgmn/
# http://www.mm288.com/mvtp/twmn/
# http://www.mm288.com/xgmn/
# http://www.mm288.com/qcmn/
# http://www.mm288.com/mnxz/
# http://www.mm288.com/swmt/
# http://www.mm288.com/mxmn/
# http://www.mm288.com/mnbz/
# http://www.mm288.com/dmmn/
# http://www.mm288.com/dmmn/cosplay/
# index : single div(id/class) -> ( no.1 a tag )| next_page : div(id/class)   http://www.mm4000.com/meinv/
# http://www.mm4000.com/meinv/  block_tag=ul,block_id=l-meinv-wrapp cl,item_tag=div,item_class=timg,children_tag=a,children_index=1,children_href=a.href,children_text=img.alt,page_tag=div,page_class=pagelists,page_key=下一页
# index : div(id/class) : ul -> li( no.1 a tag )| next_page : div(id/class)   https://www.ku66.net/r/2/index.html
# block_tag=div,block_class=TypeList,item_tag=li,item_class=,children_tag=a,children_index=1,children_href=a.href,children_text=div.innerHtml,page_tag=div,page_class=NewPages,page_key=下一页
# index : div(id/class) : ul -> li( no.1 a tag )| next_page : div(id/class)   https://www.mzitu.com/
# block_tag=ul,block_id=pins,item_tag=li,item_class=,children_tag=a,children_index=1,children_href=a.href,children_text=img.alt,page_tag=a,page_class=next page-numbers,page_key=下一页

class GroupItemSpider(object):
    def __init__(self,group_url,group_attribute,home_path):
        url_items=group_url.split('/')
        self.home_url='/'.join(url_items[0:3])
        self.group_url='/'.join(url_items[0:-1])
        if group_url.endswith(".html"):
            self.group_url = '/'.join(url_items[0:-1])
        self.block_tag=group_attribute.block_tag
        self.block_attrs=group_attribute.block_attrs
        self.item_tag=group_attribute.item_tag
        self.item_attrs=group_attribute.item_attrs
        self.children_tag=group_attribute.children_tag
        self.children_href_condition=group_attribute.children_href
        self.children_text_condition=group_attribute.children_text
        self.children_index=int(group_attribute.children_index)
        self.page_tag=group_attribute.page_tag
        self.page_attrs=group_attribute.page_attrs
        self.home_path=home_path+"/"+url_items[2].split('.')[1]
        common_filer.make_dirs(self.home_path)
        self.href_list=[]
        if common_filer.exists(self.home_path+"/href_dict.txt"):
            self.href_list=common_filer.get_file_details(self.home_path+"/href_dict.txt")
        self.summary_file_w=open(self.home_path+"/href_dict.txt","a+",encoding="utf8")
    
    def parse_page_index(self,url,html):
        page_index=common_spider.get_beautifulsoup_from_html(html,self.page_tag,attrs=self.page_attrs)
        if self.page_tag =="div":
            page_bs4=common_spider.get_beautifulsoup_from_html(str(page_index[0]),'a')
            for a_item in page_bs4:
                if str(a_item).find('下一页') !=-1 or str(a_item).find('下一张')!=-1 or str(a_item).find(">>")!=-1:
                    href_url=common_spider.get_correct_href(self.group_url, a_item)
                    return href_url
            return ""
        else:
            if page_index:
                a_item=page_index[0]
                return common_spider.get_correct_href(self.group_url, a_item)
            return ""
            
    
    def get_page_hrefs(self,url,href_dict):
        html=common_spider.get_response_text(url, '', '',3)
        href_url=self.parse_page_index(url,html)
        item_href_list=self.get_block_content(url, html)
        href_dict[url]=item_href_list
        return href_url,href_dict
        
    def get_block_content(self,url,html):
        item_href_list=[]
        block_contents=common_spider.get_beautifulsoup_from_html(html,self.block_tag,attrs=self.block_attrs)
        for block_content in block_contents:
            item_contents = common_spider.get_beautifulsoup_from_html(str(block_content), self.item_tag, attrs=self.item_attrs)
            for item_content in item_contents:
                a_child=common_spider.get_beautifulsoup_from_html(str(item_content), self.children_tag)[self.children_index-1]
                a_href_url=common_spider.get_correct_href(self.home_url, a_child)
                if self.children_text_condition == "img.alt":
                    img_item=common_spider.get_beautifulsoup_from_html(str(a_child), "img", attrs={})[0]
                    a_text_val=img_item.get("alt")
                elif self.children_text_condition == "div.innerHtml":
                    div_item=common_spider.get_beautifulsoup_from_html(str(a_child), "div", attrs={})[0]
                    a_text_val=div_item.text
                elif self.children_text_condition == "a.title":
                    a_text_val=a_child.get("title")
                else:
                    a_text_val=a_child.text
                a_text_val = a_text_val.replace("/","")
                a_text_val = a_text_val.strip()
                if F"{a_text_val}    {a_href_url}" not in self.href_list:
                    self.summary_file_w.write(F"{a_text_val}    {a_href_url}\n")
                    print(F"{a_text_val}    {a_href_url}\n")
                item_list=[a_text_val,a_href_url]
                item_href_list.append(item_list)
        return item_href_list

    def get_pages(self,href_url,href_dict):
        while href_url:
            href_url,href_dict=self.get_page_hrefs(href_url, href_dict)
        self.summary_file_w.close()
        return href_dict
    
def get_group_hrefs(group_map_attr,group_attr,group_key,home_path):
    for url_key,url_attrs in group_map_attr.items():
        for group_url in group_attr[group_key]:
            if group_url.find(url_key) !=-1:
                group_spider=GroupItemSpider(group_url,url_attrs,home_path+"/"+group_key)
                group_spider.get_pages(group_url, dict())

def download_by_key(home_path,key_category,detail_maps):
    parent_path=home_path+"/"+key_category
    key_attrs=detail_maps[key_category]
    category_paths=get_category_paths(parent_path)
    href_dict=get_href_dict(category_paths)
    download_all_items(parent_path,key_category, href_dict, key_attrs)

def get_category_paths(parent_path):
    dir_names=common_filer.get_child_files(parent_path)
    category_paths = []
    for dir_name in dir_names:
        category_path=parent_path+"/"+dir_name
        if common_filer.is_dir(category_path) and common_filer.exists(category_path+"/href_dict.txt"):
            category_paths.append(category_path)
    return category_paths
    

def download_all_items(home_path,key_category,href_dict,key_attrs):
    unorder_set=set(href_dict.keys())
    for key in unorder_set:
        val = href_dict[key]
        for url_key,url_attrs in key_attrs.items():
            if val.find(url_key)!=-1:
                download_one_item(home_path, key_category, key, val, url_attrs)

@retry(stop_max_attempt_number=30,wait_fixed=10000)
def download_one_item(home_path,key_category,key,val,url_attrs):
    current_log.info(F"{key}========{val}")
    if key_category == "picture":
        imgspider=ImgSpider(val,url_attrs['index_attrs'],url_attrs['content_attrs'],home_path,"download",key)
        imgspider.download_all_imgs()
    elif key_category == "novel":
        novelspider=NovelSpider(val,url_attrs['index_attrs'],url_attrs['content_attrs'],home_path,"download",key)
        novelspider.download_to_one_novel()
    elif key_category == "video":
        videospider=VideoSpider(val,url_attrs['index_attrs'],url_attrs['content_attrs'],home_path,"download",key)
        videospider.download_all_videos()


def get_href_dict(category_paths):
    href_dict=dict()
    for category_path in category_paths:
        file_r=open(category_path+"/href_dict.txt","r",encoding="utf8")
        for line in file_r.readlines():
            vals = line.split("    ",1)
            key_v=vals[0].strip().replace("/","")
            href_dict[key_v]=vals[1].strip().replace("\n","")
        file_r.close()
    return href_dict

def download_pictures(home_path,detail_maps):
    download_by_key(home_path, "picture", detail_maps)
    
def download_novels(home_path,detail_maps):
    download_by_key(home_path, "novel", detail_maps)

def download_videos(home_path,detail_maps):
    download_by_key(home_path, "video", detail_maps)

def download_all_spiders(home_path,detail_maps):
    key_types=['picture','novel','video']
    for key_type in key_types:
        download_by_key(home_path, key_type, detail_maps)

def download_all_spiders_one_by_random_one(home_path,detail_maps):
    parameters_list=[]
    for key_category, key_attrs in detail_maps.items():
        parent_path=home_path+"/"+key_category
        category_paths=get_category_paths(parent_path)
        href_dict=get_href_dict(category_paths)
        for href_key,href_val in href_dict.items():
            attr_key='/'.join(href_val.split("/")[0:3]).strip()+"/"
            if attr_key not in key_attrs:
                continue
            url_attrs=key_attrs[attr_key]
            spider_param=SpiderParameters(parent_path,key_category,href_key,href_val,url_attrs)
            parameters_list.append(spider_param)

    random.shuffle(parameters_list)
    for spider_param in parameters_list:
        try:
            download_one_item(spider_param.home_path, spider_param.key_category, spider_param.key, spider_param.val, spider_param.url_attrs)
        except Exception as e:
            current_log.error(e)
            time.sleep(120)
            continue
  

if __name__ == "__main__":
#     get_group_hrefs(group_map_attrs, dict_attrs, "video", "F:/Python3")
#     res=common_spider.get_response('http://icanhazip.com', '', '')
#     print(res.text)
#     download_videos("K:/Spider", detail_attrs)
    common_threadpools.run_with_limited_second(download_pictures, ["K:/Spider", detail_attrs], {}, 7200)
#     download_pictures("K:/Spider", detail_attrs)
#     download_novels("K:/Spider", detail_attrs)
#     download_all_spiders_one_by_random_one("K:/Spider", detail_attrs)
#     res=common_spider.get_response_by_seconds('http://pic3.085p.com/upload13/227899/2019/01-29/20190129134018_6126eljeqtmd_small.jpg', '', '', 3, '')
#     print(len(res.content))

#     book_url_path_map={
#         "http://www.xbiquge.la/15/15003/":'C:/Users/xcKev/eclipse-workspace/gen-tool-app/道君 .txt',
#         "http://www.xbiquge.la/21/21470/":'C:/Users/xcKev/eclipse-workspace/gen-tool-app/怪物聊天群.txt',
#         "http://www.xbiquge.la/22/22539/":'C:/Users/xcKev/eclipse-workspace/gen-tool-app/我的一天有48小时.txt',
#         "http://www.xbiquge.la/23/23930/":'C:/Users/xcKev/eclipse-workspace/gen-tool-app/我的师父很多.txt',
#         "http://www.xbiquge.la/1/1988/":'C:/Users/xcKev/eclipse-workspace/gen-tool-app/龙城.txt',
#         "http://www.xbiquge.la/15/15579/":'C:/Users/xcKev/eclipse-workspace/gen-tool-app/游戏之狩魔猎人.txt',
#         "http://www.xbiquge.la/18/18249/":'C:/Users/xcKev/eclipse-workspace/gen-tool-app/伊塔之柱.txt'}
# 
#     NovelSpider.get_novels("http://www.xbiquge.la", book_url_path_map, {'id':'list'},{'id':'content'})
