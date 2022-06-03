#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/10

@author: xcKev
'''

import requests
import time
import urllib3
import alvintools.common_tools as common
import alvintools.common_logger as log
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from alvinconst.html5tmps import HtmlTypes
from urllib.parse import urlparse,parse_qs
from selenium.webdriver.chrome.options import Options
from alvintools import common_coder, common_converter, common_tools, common_filer
from alvinwritecreater.fileswriter import SimpleFileWriter
from alvinreadparser.filesreader import SimpleFileReader
from requests.models import Response
urllib3.disable_warnings(InsecureRequestWarning)
from selenium import webdriver
import random
from alvinspider import SpiderContentItem
from retrying import retry
htmltype = HtmlTypes()

user_agent_list = htmltype.pc_user_agents
current_log=log.get_log('alvinspider', '/temp', 'alvinspider')

def get_spider_content_items(file_path):
    spider_contents=[]
    file_r=open(file_path,'r')
    for detail in file_r.readlines():
        props=detail.split(' ')
        spider_content=SpiderContentItem(props[0],props[1],props[2].replace("\n",""))
        spider_contents.append(spider_content)
    file_r.close()
    return spider_contents

def get_response_text(artifact_url,user,password,seconds,referer_url=''):
    res=get_response_by_seconds(artifact_url, user, password,seconds,referer_url)
    if res.encoding is None:
        return ""
    coding=res.encoding.lower()
    if res.apparent_encoding is not None and res.apparent_encoding != res.encoding:
        return get_utf8_response_text_with_diff_coding(res,coding,res.apparent_encoding.lower())
    return get_utf8_response_text(res, coding)

def get_response_text_with_no_encoding(artifact_url,user,password,seconds,referer_url=''):
    res=get_response_by_seconds(artifact_url, user, password,seconds,referer_url)
    if res is None or res.text is None:
        return get_response_text_with_no_encoding(artifact_url, user, password, seconds, referer_url)
    return res.text

def create_random_ip():
    global_ip_dict=dict()
    global_ip_dict[0]=9
    global_ip_dict[11]=171
    global_ip_dict[173]=191
    global_ip_dict[193]=255
    from_no = random.choice([0,11,173,193])
    a_ip = random.randint(from_no,global_ip_dict[from_no])
    b_ip = random.randint(0,255)
    c_ip = random.randint(0,255)
    d_ip = random.randint(0,255)
    ip = "%d.%d.%d.%d" % (a_ip, b_ip, c_ip, d_ip)
    return ip

def get_valid_ip():
    ip = create_random_ip()
    headers = {'User-Agent': random.choice(user_agent_list),'proxies': ip}
    try:
        response=requests.get('https://www.baidu.com',headers=headers)
        if response.status_code == 200:
            return ip
        return get_valid_ip()
    except:
        return get_valid_ip()

def get_local_ip():
    return requests.get('https://api.ipify.org/?format=json').text

def get_response_by_seconds(artifact_url,user,password,seconds,referer_url=''):
    seconds = 0
    if seconds>0:
        real_seconds=random.randint(seconds,10)
        if seconds >=10:
            real_seconds=random.randint(seconds,seconds+10)
        current_log.info(real_seconds)
        time.sleep(real_seconds)
    current_log.info(artifact_url)
    try:
        res=get_response(artifact_url, user, password,referer_url)
        response_text = get_utf8_response_text(res,"utf-8")
        if "https://www.23qb.net" in artifact_url and "出现错误！" in response_text:
            return get_none_response()
        return res
    except Exception:
        return get_none_response()

def get_none_response():
    return Response()

@retry(stop_max_attempt_number=10,wait_fixed=10000)
def get_response(artifact_url,user,password,referer_url='',proxies=''):
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    if referer_url:
        headers['Referer']=referer_url
    try:
        if user == '' and password == '':
            response = requests.get(url=artifact_url,proxies=proxies,headers=headers,timeout=30,verify=False,stream=True)
        else:
            response = requests.get(url=artifact_url,proxies=proxies,headers=headers,timeout=30,verify=False,auth=(user,password),stream=True)
        if response is not None and response.status_code == 200:
            return response
        if response.status_code != 200:
            current_log.error(artifact_url)
            raise Exception(F"{artifact_url} is not 200")
    except Exception:
        current_log.error(artifact_url)
        return get_response(artifact_url, user, password, referer_url, proxies)

@retry(stop_max_attempt_number=10,wait_fixed=10000)
def post_response(request_url,params):
    try:
        response = requests.post(request_url,params)
        if response is not None and response.status_code == 200:
            return response
    except Exception as e:
        current_log.error(e)
        return post_response(request_url, params)

def check_valid_ip(ip):
    proxies={'http':'http://'+ip}
    response=get_response('http://icanhazip.com/', '', '','',  proxies)
    if response is not None and ip.find(response.text) != -1:
        current_log.info(proxies)
        return True
    return False

def get_html_coding(url):
    html=requests.get(url)
    return html.encoding

def get_novel_response(url):
    response=get_response(url, '', '')
    return get_utf8_response_text(response,response.encoding)

def get_utf8_response_text_with_diff_coding(response,en_coding,de_coding):
    if en_coding == "gbk" or en_coding == "gb2312":
        encode_byte=response.text.encode("gbk")
    else:
        encode_byte=response.text.encode(en_coding)
    try:
        if de_coding == "gbk" or de_coding == "gb2312":
            return encode_byte.decode("gbk")
        else:
            return encode_byte.decode(de_coding)
    except:
        return encode_byte.decode("utf-8")

def get_utf8_response_text(response,coding):
    encode_byte=response.text.encode(coding)
    if coding == "gbk" or coding == "gb2312":
        try:
            return encode_byte.decode("gbk")
        except:
            return encode_byte.decode("utf-8")
    if coding == "iso-8859-1":
        try:
            return encode_byte.decode("gbk")
        except:
            return encode_byte.decode("utf-8")
    return encode_byte.decode('utf-8')

def download_m3u8(folder,m3u8_url):
    index_val=get_response_text_with_no_encoding(m3u8_url, '', '', 0)
    common_filer.make_dirs(folder)
    index_m3u8= folder+"/"+"index.m3u8"
    file_writer = SimpleFileWriter(index_m3u8)
    file_writer.append_string(index_val)
    file_writer.close()

def parse_byte_key_map_from_m3u8(index_val,parent_url):
    key_map=dict()
    for line in index_val.split('\n'):
        if "#EXT-X-KEY" in line:
            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_list=line[uri_pos:quotation_mark_pos].split('"')
            if len(key_list) == 2:
                key_path = key_list[1]
                key_url=get_real_url(parent_url, key_path)
                if not key_map:
                    res = get_response(key_url, '', '')
                    key = res.content
                    key_map['key']=key
    return key_map

def parse_ts_list_from_m3u8(index_val,parent_url):
    index_srcs=[]
    is_dicon_cnt=0
    for line in index_val.split('\n'):
        if "#EXT-X-DISCONTINUITY" in line:
            is_dicon_cnt+=1
        if line is None or line =='' or line[0] == '#':
            continue
        http_url = get_real_url(parent_url, line)
        if is_dicon_cnt%2 == 0:
            index_srcs.append(http_url)
    return index_srcs

def get_m3u8_ts_list_from_file(m3u8_file,parent_url):
    file_r = SimpleFileReader(m3u8_file)
    index_val = file_r.read()
    key_map = parse_byte_key_map_from_m3u8(index_val, parent_url)
    index_srcs=parse_ts_list_from_m3u8(index_val,parent_url)
    return key_map,index_srcs

def get_m3u8_ts_list(folder,m3u8_url):
    parent_url="/".join(m3u8_url.split("/")[:-1])
    download_m3u8(folder,m3u8_url)
    return get_m3u8_ts_list_from_file(folder+"/index.m3u8",parent_url)

def download_ts(video_src,folder,ts_name):
    cur_file=folder+'/'+ts_name
    if common_filer.is_file(cur_file) and common_filer.get_file_size(cur_file)>0:
        return
    file_w=open(cur_file,'wb')
    current_log.info(video_src)
    response = get_response(video_src, '', '')
    try:
        print(len(response.content))
        if response.content is not None and len(response.content) > 0:
            file_w.write(response.content)
        else:
            file_w.close()
    except:
        file_w.close()
    file_w.close()

def get_url_params(url):
    parsed=urlparse(url)
    return parse_qs(parsed.query,True)

def get_iframe_src(url):
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    driver=webdriver.Chrome('F:/Python3/chromedriver',chrome_options)
    driver.get(url)
    iframe = driver.find_element_by_xpath("//iframe[contains(@src,'*******************/index.m3u8'")
    src = iframe.get_attribute("src")
    driver.close()
    return src

def get_javascript_text(home_url,script_item):
    script_src=script_item.get('src')
    if script_src is None:
        return common_coder.str2unicode(script_item.text).replace("\/","/")
    script_url=script_src
    if script_src[0] =="/":
        script_url=get_url(home_url, script_src)
    return get_response_text(script_url,'','',0,home_url)
    
def get_javascript_vals(script_text):
    js_lines=script_text.split(";")
    if not js_lines:
        js_lines=[script_text]
    for js_line in js_lines:
        if js_line.find("=")==-1:
            continue
        js_val=js_line.split("=",1)[-1]
        if (js_val[0]=="'" and js_val[-1]=="'") or (js_val[0]=='"' and js_val[-1]=='"'):
            js_val=js_val[1:-1]
        return js_val
    return ""

def get_javascript_index_m3u8(script_text):
    js_val=get_javascript_vals(script_text)
    current_log.info(js_val.find("/index.m3u8"))
    js_val=js_val.strip()
    if js_val.find("/index.m3u8")!=-1 and ((js_val[0]=="{" and js_val[-1] =="}") or (js_val[0]=="[" and js_val[-1] =="]")):
        index_m3u8_dict = common_converter.json_to_dict(js_val)
        return common_tools.find_vals_from_dict_by_keystr(index_m3u8_dict, "/index.m3u8", [])
    return js_val

def get_correct_href(url,a_item):
    href=a_item.get('href')
    return get_real_url(url,href)

def get_real_url(home_url,href_url):
    if href_url[0] == '/':
        parent_url = '/'.join(home_url.split('/')[0:3])
        href_url = href_url[1:]
        return get_url(parent_url,href_url)
    return get_url(home_url,href_url)

def get_url(parent_url,href_url):
    if href_url is None:
        return ''
    if common.is_http_url(href_url):
        return href_url
    return common.get_home_path(parent_url)+href_url

def get_beautifulsoup_from_html(html_text,tag_name,attrs={}):
    bs4 = BeautifulSoup(html_text,'html.parser')
    if len(attrs) == 0:
        items = bs4.find_all(tag_name)
    else:
        items = bs4.find_all(tag_name, attrs=attrs)
    return items

def get_beautifulsoup_from_html_without_tag(html_text):
    bs4 = BeautifulSoup(html_text,'html.parser')
    return bs4.body.children

def is_invalid_a_item(a_item):
    item_name=a_item.text
    a_href=a_item.get('href')
    return a_href is None or item_name is None or len(a_href)==0 or a_href[0]=='#' or item_name=='../'

def is_invalid_a_href(a_href):
    return a_href is None or len(a_href)==0 or a_href[0]=='#'

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
        if is_invalid_a_item(a_item):
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

def get_all_a_hrefs(server_urls,all_a_list):
    running_a_list=[]
    all_a_list=common.to_unique_list(all_a_list)
    for server_url in server_urls:
        html=get_response_text(server_url, '', '')
        a_items=get_beautifulsoup_from_html(html, 'a')
        for a_item in a_items:
            a_href = a_item.get('href')
            if is_invalid_a_href(a_href):
                continue
            if a_href[0]=='/':
                a_href = get_url(server_url,a_href[1:])
                all_a_list.append(a_href)
                running_a_list.append(a_href)
    return get_all_a_hrefs(running_a_list, all_a_list)
    
def add_to_list(all_a_list, home_server, a_list):
    for a_item in a_list:
        a_href = a_item.get('href')
        if is_invalid_a_href(a_href):
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

def get_parent_url(a_url):
    return "/".join(a_url.split('/')[:-1])

def get_new_servers_from_menu_attrs(servers, menu_cnt):
    new_servers = servers+[]
    for index, server in enumerate(servers):
        url = get_parent_url(server)
        head_url = server.split('/')[-1].replace("_1.html", "")
        page_count = menu_cnt[index]
        for pg_cnt in range(2, page_count):
            new_servers.append(url + "/" + head_url + "_" + str(pg_cnt) + ".html")
    return new_servers
