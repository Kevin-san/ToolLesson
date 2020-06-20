#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/30

@author: xcKev
'''

from os.path import getsize,join
import tools.common_logger as log
import tools.common_tools as common
import os
import time
import chardet
import sys


current_log=log.get_log('filer', '/temp', 'filer')

def get_file_name(file_path):
    return os.path.basename(file_path)

def get_file_c_date(file_path):
    file_date=time.localtime(os.stat(file_path).st_ctime)
    return time.strftime('%Y-%m-%d %H:%M:%S',file_date)

def get_file_m_date(file_path):
    file_date=time.localtime(os.stat(file_path).st_mtime)
    return time.strftime('%Y-%m-%d %H:%M:%S',file_date)

def get_child_files(file_path):
    return os.listdir(file_path)

def get_file_dir_size(directory):
    if os.path.isfile(directory):
        return getsize(directory)
    size = 0
    for root,dirs,files in os.walk(directory):
        size+=sum([getsize(join(root,name)) for name in files])
    return size

def get_file_encoding(file_path):
    file_h = open(file_path,'rb')
    file_read = file_h.read()
    file_char_info = chardet.detect(file_read)
    return file_char_info['encoding']

def recur_file_infos(local_xenv_home,all_files):
    try:
        fils_list=os.listdir(local_xenv_home)
    except PermissionError as err:
        print(err)
        fils_list=[]
    for file_name in fils_list:
        file_abs_path=os.path.join(local_xenv_home,file_name)
        if os.path.isdir(file_abs_path):
            recur_file_infos(file_abs_path, all_files)
        else:
            all_files.append(file_abs_path)

def make_sub_file(lines,src_name,sub):
    [des_filename,extname]=os.path.splitext(src_name)
    filename=des_filename+'_'+str(sub)+extname
    fout=open(filename,'w')
    try:
        fout.writelines(lines)
        return sub+1
    finally:
        fout.close()

def split_big_file_by_count(file_name,count):
    fin=open(file_name,'r')
    try:
        buf=[]
        sub=1
        for line in fin:
            buf.append(line)
            if len(buf)==count:
                sub=make_sub_file(buf, file_name, sub)
                buf=[]
        if len(buf)!=0:
            sub=make_sub_file(buf, file_name, sub)
    finally:
        fin.close()

def get_file_details(file_path):
    try:
        file_h = open(file_path,'r')
        text_lines = file_h.read().splitlines()
        return text_lines
    except IOError as error:
        current_log.error(F'Read input file Error:{error}')
        sys.exit()

def get_file_infos_service(local_xenv_home,local_home):
    path_list=[]
    current_log.info('start time:',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    recur_file_infos(local_xenv_home,path_list)
    dir_list,file_list=common.get_directory_file_list(path_list)
    arti_f=open(local_home+'/xenv.txt','w+')
    for index,dir_name in enumerate(dir_list):
        arti_f.write(F'{dir_name}={file_list[index]}\n')
    current_log.info('end time:',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))