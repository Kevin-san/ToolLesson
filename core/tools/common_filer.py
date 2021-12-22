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
import shutil
from natsort.natsort import natsorted
from retrying import retry
from Crypto.Cipher import AES
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import zipfile


current_log=log.get_log('filer', log.LOG_DIR, 'filer')

def get_stream_data(file_path):
    current_log.info(F'read {file_path}')
    stream_reader = open(file_path,'rb')
    stream_data = stream_reader.read()
    stream_reader.close()
    return stream_data

def get_file_name(file_path):
    return os.path.basename(file_path)

def get_parent_dir(file_path):
    return os.path.dirname(file_path)

def get_file_c_date(file_path):
    file_date=time.localtime(os.stat(file_path).st_ctime)
    return time.strftime('%Y-%m-%d %H:%M:%S',file_date)

def get_file_m_date(file_path):
    file_date=time.localtime(os.stat(file_path).st_mtime)
    return time.strftime('%Y-%m-%d %H:%M:%S',file_date)

def get_child_files(file_path):
    return os.listdir(file_path)

def get_child_absolute_files(file_path):
    paths=[]
    for file in os.listdir(file_path):
        paths.append(file_path+'/'+file)
    return paths

def get_child_absolute_files_exclude_spec_files(file_path,spec_files):
    paths=[]
    for file in os.listdir(file_path):
        if file not in spec_files:
            paths.append(file_path+'/'+file)
    return paths

def is_file(file_path):
    return os.path.isfile(file_path)

def exists(file_path):
    return os.path.exists(file_path)

def is_dir(dir_path):
    return os.path.isdir(dir_path)

def move_file(file_path,to_path):
    return shutil.move(file_path,to_path)

def make_dirs(directory):
    if os.path.isdir(directory):
        return True
    return os.makedirs(directory)

def add_files_into_zip(absolute_file_path_list,zip_path):
    zip_file = zipfile.ZipFile(zip_path,'w')
    for file_path in absolute_file_path_list:
        zip_file.write(file_path,file_path,zipfile.ZIP_DEFLATED)
    zip_file.close()

def file_iterator(file_name, chunk_size=2048):
    f=open(file_name,'rb')
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break

def get_file_size(file_path):
    return getsize(file_path)

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

def create_category_dir(home_dir,category,name):
    folder=home_dir+'/'+category+'/'+name
    make_dirs(folder)
    return folder

def merge_ts_files(ts_dir,key_map,ts_path):
    files=get_child_absolute_files(ts_dir)
    files = natsorted(files)
    ts_path_h=open(ts_path,'ab+')
    for file in files:
        tmp_file=open(file,'rb+')
        if key_map:
            key = key_map['key']
            cryptor = AES.new(key, AES.MODE_CBC)
            ts_path_h.write(cryptor.decrypt(tmp_file.read()))
        else:
            ts_path_h.write(tmp_file.read())
        tmp_file.close()
    ts_path_h.close()
    mp4_path=to_mp4_files(ts_path)
#     os.remove(ts_path)
#     remove_dir(ts_dir)
    return mp4_path

def to_mp4_files(ts_file):
    mp4_path=ts_file.replace(".ts",".mp4")
    ffmpeg_path=common.get_ffmpeg_cmd()
    cmd = ffmpeg_path + " -i " + ts_file + " -c copy " + mp4_path
    os.system(cmd)
    return mp4_path

def merget_ts_files_without_key(ts_dir,ts_path):
    files=get_child_absolute_files_exclude_spec_files(ts_dir,['index.m3u8'])
    files = natsorted(files)
    ts_path_h=open(ts_path,'ab+')
    for file in files:
        tmp_file=open(file,'rb+')
        ts_path_h.write(tmp_file.read())
        tmp_file.close()
    ts_path_h.close()
    mp4_path=to_mp4_files(ts_path)
    os.remove(ts_path)
#     remove_dir(ts_dir)
    return mp4_path

def merge_ts_and_to_mp4(parent_folder):
    list_children_dirs = get_child_absolute_files(parent_folder)
    index_path=parent_folder+"/index.txt"
    index_path_h= open(index_path,'a+')
    for dir_path in list_children_dirs:
        if is_dir(dir_path):
            ts_file = dir_path + ".ts"
            mp4_file = merget_ts_files_without_key(dir_path, ts_file)
            index_path_h.write(mp4_file+"\n")
    index_path_h.close()
            

def get_file_total_time(file_path,file_type):
    if file_type == 'audio':
        audio_type = file_path.split(".")[-1]
        sound = AudioSegment.from_file(file_path,audio_type)
        return sound.duration_seconds
    else:
        clip = VideoFileClip(file_path)
        return clip.duration

def remove_files(file_list):
    for file in file_list:
        os.remove(file)

def remove_dir(dir_path):
    shutil.rmtree(dir_path)

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

def get_dict_from_file(file_path):
    dict_result=dict()
    file_r=open(file_path,"r",encoding='utf8')
    line_list=file_r.readlines()
    for line in line_list:
        line_vals=line.split(" ",1)
        line_key=line_vals[1].replace('\n','')
        href_url=line_vals[0]
        dict_result[line_key]=href_url
    file_r.close()
    return dict_result

def get_file_details_by_encoding(file_path,encoding):
    try:
        if encoding.lower() == "gb2312":
            encoding = "gbk"
        file_h = open(file_path,'r',encoding=encoding)
        text_lines = file_h.read().splitlines()
        file_h.close()
        return text_lines
    except IOError as error:
        current_log.error(F'Read input file Error:{error}')
        sys.exit()

def get_file_details(file_path):
    try:
        file_h = open(file_path,'r',encoding="utf-8")
        text_lines = file_h.read().splitlines()
        file_h.close()
        return text_lines
    except IOError as error:
        current_log.error(F'Read input file Error:{error}')
        sys.exit()
@retry(stop_max_attempt_number=5,wait_fixed=10000)
def get_file_detail(file_path):
    try:
        file_h = open(file_path,'r',encoding="utf-8")
        text_line = file_h.read()
        file_h.close()
        return text_line
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