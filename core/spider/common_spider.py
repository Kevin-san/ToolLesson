#-*-coding:utf-8-*-
'''
Created on 2019/6/10

@author: xcKev
'''


import requests
import random
import os
import re
import urllib3
import tools.common_tools as common
import tools.common_logger as log
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from const.html5tmps import HtmlTypes

urllib3.disable_warnings(InsecureRequestWarning)

htmltype = HtmlTypes()

user_agent_list = htmltype.pc_user_agents
current_log=log.get_log('spider', '/temp', 'spider')



def get_response_text(artifact_url,user,password):
    res=get_response(artifact_url, user, password)
    res_text = ''
    if res is not None:
        res_text =res.text
    return res_text
        
def get_response(artifact_url,user,password,referer_url=''):
    user_agent = random.choice(user_agent_list)
    if referer_url != '':
        headers = { 'User-Agent': user_agent ,
               'Referer':referer_url
               }
    else:
        headers = {'User-Agent': user_agent}
    try:
        if user == '' and password == '':
            response = requests.get(url=artifact_url,headers=headers,verify=False)
        else:
            response = requests.get(url=artifact_url,headers=headers,verify=False,auth=(user,password))
        return response
    except Exception:
        return None

def get_url(parent_url,href_url):
    if href_url is None:
        return ''
    if common.is_http_url(href_url):
        return href_url
    return common.get_home_path(parent_url)+href_url

def get_novel_response(url):
    response = get_response(url, '', '')
    return response.text.encode('iso-8859-1').decode('utf-8')

def get_beautifulsoup_from_html(html_text,tag_name,attrs={}):
    bs4 = BeautifulSoup(html_text,'html.parser')
    if len(attrs) == 0:
        items = bs4.find_all(tag_name)
    else:
        items = bs4.find_all(tag_name, attrs=attrs)
    return items

def get_novel_titles(server,url,attrs):
    html = get_novel_response(url)
    div = get_beautifulsoup_from_html(html,'div', attrs=attrs)
    a_list = get_beautifulsoup_from_html(str(div[0]),'a')
    title_nms=[]
    title_hrefs=[]
    for a_it in a_list:
        title_nms.append(a_it.text)
        title_hrefs.append(server+a_it.get('href'))
    return title_nms,title_hrefs

def get_novel_details(url,attrs):
    html = get_novel_response(url)
    texts = get_beautifulsoup_from_html(html,'div', attrs=attrs)
    texts = texts[0].text.replace('\xa0'*8,'\n\n')
    return texts

def get_novel(server,url,write_path,tit_attrs,det_attrs):
    title_nms,title_hrefs=get_novel_titles(server,url,tit_attrs)
    novel_h=open(write_path,'a+',encoding='utf8')
    for index,tit_nm in enumerate(title_nms):
        name=tit_nm
        novel_content=get_novel_details(title_hrefs[index], det_attrs)
        novel_h.write('\n\n'+name+'\n'+novel_content)

def get_artifact_info(artifact_url,user,password):
    artifact_url=common.get_home_path(artifact_url)
    html=get_response_text(artifact_url, user, password)
    a_list=get_beautifulsoup_from_html(html,'a')
    a_href_list=[]
    a_name_list=[]
    for a_item in a_list:
        if a_item == '../':
            continue
        a_name_list.append(a_item.text)
        a_href = a_item.get('href')
        href_url = get_url(artifact_url, a_href)
        a_href_list.append(href_url)
    return a_name_list,a_href_list

def get_artifact_infos(a_name_list,a_href_list,user='',password=''):
    if common.is_file(a_name_list):
        return a_name_list,a_href_list
    new_href_list=[]
    new_name_list=[]
    for index,a_name in enumerate(a_name_list):
        arti_url=a_href_list[index]
        child_name_list,child_href_list=get_artifact_info(arti_url, user, password)
        if len(child_name_list) ==0:
            new_name_list.append(a_name)
            new_href_list.append(arti_url)
            continue
        for index in range(0,len(child_name_list)):
            child_name=child_name_list[index]
            child_href=child_href_list[index]
            new_name_list.append(a_name+child_name)
            new_href_list.append(child_href)
    return get_artifact_infos(new_name_list, new_href_list, user, password)

def get_download_artifacts_infos(artifactory,local_home,user,password):
    local_home=common.get_home_path(local_home)
    a_name_list,a_href_list=get_artifact_info(artifactory, user, password)
    final_a_name_list,final_a_href_list=get_artifact_infos(a_name_list, a_href_list, user, password)
    return final_a_name_list,final_a_href_list

def write_artifacts_info_into_artitext(local_home,a_name_list):
    dir_list,file_list=common.get_directory_file_list(a_name_list)
    os.makedirs(local_home)
    arti_f=open(local_home+'artifacts.txt','w+')
    for index,dir_name in enumerate(dir_list):
        arti_f.write(dir_name+'='+file_list[index]+'\n')
    arti_f.close()

def download_files_from_url(local_home,a_name_list,a_href_list,user,password):
    for index,path_name in enumerate(a_name_list):
        directory,file_name=common.get_dir_file(path_name)
        if not os.path.exists(local_home+directory):
            os.makedirs(local_home+directory)
        download_url=a_href_list[index]
        res=get_response(download_url, user, password)
        file_w=open(local_home+file_name,'wb')
        file_w.write(res.content)
        file_w.close()

def download_artifacts(artifactory,local_home,user,password):
    final_a_name_list,final_a_href_list=get_download_artifacts_infos(artifactory,local_home, user, password)
    write_artifacts_info_into_artitext(local_home, final_a_name_list)
    download_files_from_url(local_home, final_a_name_list,final_a_href_list, user, password)

def download_artifacts_service():
    artifact_url=os.getenv('ARTI')
    user=os.getenv('SOEID')
    password=os.getenv('PASSWORD')
    local_home=os.getenv('LOCAL_ARTI')
    download_artifacts(artifact_url, local_home, user, password)

def is_valid_a_item(a_item):
    item_name=a_item.text
    a_href=a_item.get('href')
    return a_href is None or item_name is None or len(a_href)==0 or a_href[0]=='#' or item_name=='../'

def is_valid_a_href(a_href):
    return a_href is None or len(a_href)==0

def get_a_info(server,url,user,password):
    real_url=common.get_home_path(url)
    html=get_response_text(real_url, user, password)
    if html == '':
        return [],[]
    a_list=get_beautifulsoup_from_html(html,'a')
    a_name_list=[]
    a_href_list=[]
    for a_item in a_list:
        item_name=a_item.text
        a_href=a_item.get('href')
        if is_valid_a_item(a_item):
            continue
        if a_href[0]=='/':
            a_href=a_href[1:]
        href_url=get_url(server, a_href)
        if href_url =='':
            continue
        a_name_list.append(item_name)
        a_href_list.append(href_url)
    return common.to_unique_list(a_name_list),common.to_unique_list(a_href_list)

def get_a_infos(server,a_name_list,a_href_list,user,password,count):
    if len(a_name_list)>count:
        return a_name_list,a_href_list
    new_href_list=a_href_list
    new_name_list=a_name_list
    for index in range(0,len(a_name_list)):
        url=a_href_list[index]
        child_name_list,child_href_list=get_a_info(server, url, user, password)
        if len(child_name_list)==0:
            continue
        new_name_list=common.to_unique_list(new_name_list+child_name_list)
        new_href_list=common.to_unique_list(new_href_list+child_href_list)
    if len(new_name_list) == len(a_name_list) and len(new_href_list)==len(a_href_list):
        return new_name_list,new_href_list
    return get_a_infos(server, new_name_list,new_href_list, user, password, count)

def download_img_by_condition(url,page_attrs,pic_attrs,home_path,name,count):
    if count ==0:
        return
    referer_url = url
    page_infos=get_img_page_info(url,[], page_attrs, count)
    directory=home_path+'/'+name
    cnt = 1
    if not os.path.exists(directory):
        os.makedirs(directory)
    for page_info in page_infos:
        img_src=get_img_pic_info(page_info, pic_attrs)
        img_name=name+'_'+str(cnt)+'.'+img_src.split('/')[-1].split('.')[-1]
        res=get_response(img_src, '','',referer_url)
        file_w=open(directory+'/'+img_name,'wb')
        file_w.write(res.content)
        file_w.close()
        print(cnt)
        cnt = cnt+1

def download_imgs(directory,name,img_url,referer_url):
    img_name=name+'.'+img_url.split('/')[-1].split('.')[-1]
    res=get_response(img_url, '','',referer_url)
    file_w=open(directory+'/'+img_name,'wb')
    file_w.write(res.content)
    file_w.close()

def get_all_home_servers(servers,div_attrs):
    new_servers = [] + servers
    for server in servers:
        html=get_response_text(server, '', '')
        div_pages=get_beautifulsoup_from_html(html,'div',attrs=div_attrs)
        a_hrefs = get_beautifulsoup_from_html(str(div_pages[0]),'a')
        for a_item in a_hrefs:
            a_href = a_item.get('href')
            new_servers.append(a_href)
    return common.to_unique_list(new_servers)

def get_all_a_href_list(servers,div_attrs):
    all_a_list=[]
    for server in servers:
        html=get_response_text(server, '', '')
        div_items=get_beautifulsoup_from_html(html,'div',attrs=div_attrs)
        ul_items = get_beautifulsoup_from_html(str(div_items[0]),'ul')
        for ul_it in ul_items:
            a_list=get_beautifulsoup_from_html(str(ul_it),'a')
            for a_item in a_list:
                a_href = a_item.get('href')
                all_a_list.append(a_href)
    return common.to_unique_list(all_a_list)


def add_to_list(all_a_list, home_server, a_list):
    for a_item in a_list:
        a_href = a_item.get('href')
        if is_valid_a_href(a_href):
            continue
        if a_href[0]=='/':
            a_href = get_url(home_server,a_href[1:])
        all_a_list.append(a_href)

def get_all_a_href_list_from_dup_divs(servers,home_server,div_attrs):
    all_a_list=[]
    for server in servers:
        html=get_response_text(server, '', '')
        html_bs4=BeautifulSoup(html,'html.parser')
        for div_attr in div_attrs:
            div_items=html_bs4.find_all('div',attrs=div_attr)
            for div_bs in div_items:
                ul_items = get_beautifulsoup_from_html(str(div_bs),'ul')
                for ul_it in ul_items:
                    a_list=get_beautifulsoup_from_html(str(ul_it),'a')
                    add_to_list(all_a_list, home_server, a_list)
    return common.to_unique_list(all_a_list)

def get_img_page_info(url,page_infos,page_attrs,count,is_end=False):
    page_infos.append(url)
    page_infos = common.to_unique_list(page_infos)
    last_count = len(page_infos)
    if last_count==count:
        return page_infos
    server = url
    if url.endswith('.html'):
        server = get_parent_url(url)
    html=get_response_text(url, '', '')
    div_page=get_beautifulsoup_from_html(html,'div',attrs=page_attrs)
    page_bs4=get_beautifulsoup_from_html(str(div_page[0]),'a')
    count_text = str(count)
    for page_a in page_bs4:
        href=page_a.get('href')
        text_value = page_a.text
        if is_end:
            count_text = str(count-1)
        if is_valid_a_href(href) or not text_value.isdigit() or text_value == count_text or href == '#':
            continue
        if href[0]=='/':
            href=href[1:]
        href_url=get_url(server, href)
        page_infos.append(href_url)
    page_infos = common.to_unique_list(page_infos)
    if len(page_infos) == count-1:
        return get_img_page_info(page_infos[-1],page_infos,page_attrs,count,True)
    else:
        return get_img_page_info(page_infos[-1],page_infos,page_attrs,count)

def get_img_pic_info(url,pic_attrs):
    html=get_response_text(url, '', '')
    div_pic=get_beautifulsoup_from_html(html,'div',attrs=pic_attrs)
    pic_bs4=get_beautifulsoup_from_html(str(div_pic[0]),'img')
    img_src=pic_bs4[0].get('src')
    img_url=pic_bs4[0].get('url')
    if img_url is not None and img_url != img_src:
        img_src = img_url
    return img_src

def get_mzitu_imgs(count=-1):
    mzitu_server='https://www.mzitu.com/all/'
    html=get_response_text(mzitu_server, '', '')
    ul_items=get_beautifulsoup_from_html(html,'ul',attrs={'class':'archives'})
    all_a_list=[]
    for ul_it in ul_items:
        a_list=get_beautifulsoup_from_html(str(ul_it),'a')
        all_a_list=all_a_list+a_list
    for index,a_item in enumerate(all_a_list):
        a_url = a_item.get('href')
        res=get_response_text(a_url, '','')
        span_list= get_beautifulsoup_from_html(res,'span')
        count_list=[]
        for span_it in span_list:
            count_val=span_it.text
            if count_val.isdigit():
                count_list.append(int(count_val))
        if count > 0:
            count = common.get_lower_num(count,count_list[-1])
            download_img_by_condition(a_url, {'class':'pagenavi'}, {'class':'main-image'}, 'F:/Python3/picture', 'mzitu'+str(index), count)
            count = count - count_list[-1] if count > count_list[-1] else 0
        else:
            download_img_by_condition(a_url, {'class':'pagenavi'}, {'class':'main-image'}, 'F:/Python3/picture', 'mzitu'+str(index), count_list[-1])

def get_win4000_imgs(img_count=-1):
    win4000_servers = [
"http://www.win4000.com/meinvtag2_1.html",
"http://www.win4000.com/meinvtag3_1.html",
"http://www.win4000.com/meinvtag4_1.html",
"http://www.win4000.com/meinvtag5_1.html",
"http://www.win4000.com/meinvtag6_1.html",
"http://www.win4000.com/meinvtag7_1.html",
"http://www.win4000.com/meinvtag26_1.html"
        ]
    new_win4000_servers = get_all_home_servers(win4000_servers, {'class':'pages'})
    all_a_list = get_all_a_href_list(new_win4000_servers, {'class':'list_cont Left_list_cont Left_list_cont2'})
    for index,a_url in enumerate(all_a_list):
        directory = 'F:/Python3/picture/win4000_'+str(index)
        if not os.path.exists(directory):
            os.makedirs(directory)
        a_org_url = a_url.replace(".html","")
        res=get_response_text(a_url, '','')
        div_bs4 = get_beautifulsoup_from_html(res,"div", attrs={'class':'ptitle'})
        em_bs4  = get_beautifulsoup_from_html(str(div_bs4),'em')
        em_str = re.sub("\D","",str(em_bs4[0]))
        print(em_str)
        count = int(em_str)
        cnt = 0
        for cnt_id in range(1,count):
            if cnt_id >1:
                a_url = a_org_url+"_"+str(cnt_id)+".html"
            img_src = get_img_pic_info(a_url, {'id':'pic-meinv'})
            download_imgs(directory, 'win4000_'+str(cnt_id), img_src,"http://www.win4000.com")
            cnt = cnt+1
            if cnt == img_count:
                return


def makedirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_new_servers_from_menu_attrs(servers, menu_cnt):
    new_servers = servers+[]
    for index, server in enumerate(servers):
        url = get_parent_url(server)
        head_url = server.split('/')[-1].replace("_1.html", "")
        page_count = menu_cnt[index]
        for pg_cnt in range(2, page_count):
            new_servers.append(url + "/" + head_url + "_" + str(pg_cnt) + ".html")
    return new_servers


def get_parent_url(a_url):
    return "/".join(a_url.split('/')[:-1])

def get_7160_imgs(count=-1):
    servers = [
        "https://www.7160.com/xingganmeinv/list_3_1.html",
        "https://www.7160.com/rentiyishu/list_1_1.html"
        ]
    menu_cnt = [329,100]
    new_servers= get_new_servers_from_menu_attrs(servers, menu_cnt)
    all_a_list = get_all_a_href_list_from_dup_divs(new_servers, "https://www.7160.com/",[{"class":"new-img"},{"class":"new-img lastimg"}])
    for index,a_url in enumerate(all_a_list):
        directory = 'F:/Python3/picture/7160_'+str(index)
        makedirs(directory)
        res=get_response_text(a_url, '','')
        div_itempage= get_beautifulsoup_from_html(res,'div',attrs={"class":"itempage"})
        page_bs4=get_beautifulsoup_from_html(str(div_itempage[0]),'a')
        cnt=0
        for page_a in page_bs4:
            href=page_a.get('href')
            text_value = page_a.text
            if text_value.isdigit() and int(text_value)==1 and href == '#':
                href = a_url
            elif is_valid_a_href(href) or not text_value.isdigit() or href == '#':
                continue
            if href[0]=='/':
                href=href[1:]
            href_url=get_url(a_url, href)
            img_src = get_img_pic_info(href_url, {"class":"picsbox picsboxcenter"})
            download_imgs(directory, "7160_"+text_value, img_src, "/".join(a_url.split('/')[:-1]))
            cnt = cnt+1
            if cnt == count :
                return
# if __name__ == "__main__":
#     novels=get_novel("http://www.xbiquge.la","http://www.xbiquge.la/15/15003/",'C:/Users/xcKev/eclipse-workspace/gen-tool-app/道君 .txt', {'id':'list'},{'id':'content'})
 
 
if __name__=='__main__':
#     download_img_by_condition('https://www.2717.com/ent/meinvtupian/2019/314009.html', {'class':'page-tag oh'}, {'class':'articleV4Body','id':'picBody'}, 'C:/Users/xcKev/eclipse-workspace/gen-tool-app/picture', 'test2', 40)
#     download_img_by_condition('https://www.2717.com/ent/meinvtupian/2019/313997.html', {'class':'page-tag oh'}, {'class':'articleV4Body','id':'picBody'}, 'C:/Users/xcKev/eclipse-workspace/gen-tool-app/picture', 'test2', 63)
#     download_img_by_condition('https://www.2717.com/ent/meinvtupian/2019/313938.html', {'class':'page-tag oh'}, {'class':'articleV4Body','id':'picBody'}, 'C:/Users/xcKev/eclipse-workspace/gen-tool-app/picture', 'test3', 35)
#     download_img_by_condition('https://www.mzitu.com/183043', {'class':'pagenavi'}, {'class':'main-image'}, 'C:/Users/xcKev/eclipse-workspace/gen-tool-app/picture', 'test4', 65)
#     get_7160_imgs(-1)
#     novels=get_novel("http://www.xbiquge.la","http://www.xbiquge.la/21/21470/",'C:/Users/xcKev/eclipse-workspace/gen-tool-app/怪物聊天群.txt', {'id':'list'},{'id':'content'})
    novels=get_novel("http://www.xbiquge.la","http://www.xbiquge.la/22/22539/",'C:/Users/xcKev/eclipse-workspace/gen-tool-app/我的一天有48小时.txt', {'id':'list'},{'id':'content'})
    novels=get_novel("http://www.xbiquge.la","http://www.xbiquge.la/23/23930/",'C:/Users/xcKev/eclipse-workspace/gen-tool-app/我的师父很多.txt', {'id':'list'},{'id':'content'})
    novels=get_novel("http://www.xbiquge.la","http://www.xbiquge.la/1/1988/",'C:/Users/xcKev/eclipse-workspace/gen-tool-app/龙城.txt', {'id':'list'},{'id':'content'})
    novels=get_novel("http://www.xbiquge.la","http://www.xbiquge.la/15/15579/",'C:/Users/xcKev/eclipse-workspace/gen-tool-app/游戏之狩魔猎人.txt', {'id':'list'},{'id':'content'})
    novels=get_novel("http://www.xbiquge.la","http://www.xbiquge.la/18/18249/",'C:/Users/xcKev/eclipse-workspace/gen-tool-app/伊塔之柱.txt', {'id':'list'},{'id':'content'})

