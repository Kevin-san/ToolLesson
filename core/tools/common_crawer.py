# -*- coding: UTF-8 -*-
'''
Created on 2021/01/02

@author: xcKev
'''
import struct
import socket
from tools import common_filer
import urllib
import os

def ip2int(ip_str):
    return struct.unpack('!I', socket.inet_aton(ip_str)[0])

def int2ip(ip_int):
    return socket.inet_ntoa(struct.pack('!I',ip_int))

def download_files_by_urls(url_list,default_dir):
    common_filer.make_dirs(default_dir)
    for url in url_list:
        filename = url.split('/')[-1]
        save_path = os.path.join(default_dir, filename)
        urllib.request.urlretrieve(url, save_path)
    
