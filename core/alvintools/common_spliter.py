#-*- encoding:UTF-8 -*-
'''
Created on 2021/7/11

@author: xcKev
'''
from alvintools import common_filer


def split_chapter_names(trim_line):
    line_list = trim_line.split(" ")
    if len(line_list) == 1:
        line_list = trim_line.split("：")
    return line_list

def is_novel_title(trim_line):
    line_list = split_chapter_names(trim_line)
    for line_str in line_list:
        if is_novel_chapter(line_str):
            return True
    return False

def get_novel_chapter(trim_line):
    line_list = split_chapter_names(trim_line)
    for line_id,line_str in enumerate(line_list):
        if is_novel_chapter(line_str):
            return " ".join(line_list[line_id:]).replace("?","")

def is_novel_chapter(line_str):
    return (line_str.startswith("第") and line_str.endswith("章")) or (line_str.startswith("第") and line_str.endswith("节")) or ("第" in line_str and line_str.endswith("章")) or line_str.isnumeric()

def split_txt_novel_to_chapter(file_path):
    dir_path = file_path.replace(".txt","")
    common_filer.make_dirs(dir_path)
    index_file = dir_path+"/小说目录.txt"
    index_h = open(index_file,'a+',encoding="utf-8")
    file_encoding = common_filer.get_file_encoding(file_path)
    novel_lines = common_filer.get_file_details_by_encoding(file_path,file_encoding)
    chapter_path = dir_path+"/序.txt"
    for novel_line in novel_lines:
        trim_line = novel_line.strip().replace("\\","").replace("\r","").replace("）",")").replace("（","(")
        trim_line = trim_line.replace("(www.yxgxsw.com-云轩阁)：ｗàｐ.1⑹κx  s.ｃOM  文字版首发","")
        try:
            if trim_line.startswith("更新时间：") or trim_line == "全文字更新，TXT下载，尽在 小说骑士 http://www.xs74.com/" or trim_line == "":
                continue
            elif is_novel_title(trim_line):
                novel_chapter = get_novel_chapter(trim_line)
                index_h.write(novel_chapter)
                chapter_path = dir_path+"/"+ novel_chapter+".txt"
                print(chapter_path)
            else:
                chapter_h=open(chapter_path,'a+',encoding="utf-8")
                chapter_h.write(trim_line+"\n")
                chapter_h.close()
        except Exception as e:
            print(e)
    index_h.close()


def recur_split_novels_in_novel_parent_dir(dir_path):
    file_list = common_filer.get_child_absolute_files(dir_path)
    for file_path in file_list:
        if file_path.endswith(".txt"):
            split_txt_novel_to_chapter(file_path)
    
            
    