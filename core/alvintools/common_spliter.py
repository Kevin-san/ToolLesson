#-*- encoding:UTF-8 -*-
'''
Created on 2021/7/11

@author: xcKev
'''
from alvintools import common_filer
import re
from alvinreadparser.pdfreader import SimplePdfReader
from alvinwritecreater.fileswriter import SimpleFileWriter
from alvinreadparser.filesreader import SimpleFileReader

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
            return " ".join(line_list[line_id:]).replace("?","").replace("：","").replace(" ","")

def is_novel_chapter(line_str):
    line_str = line_str.strip()
    match_obj = re.search(r'^第(\s*)([一二三四五六七八九十百千0123456789]*)(\s*)([章节回页]{1})(\s*)(.*)',line_str,re.M|re.I)
    if match_obj:
        print(line_str)
        return True
    return False

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
        try:
            if is_novel_title(trim_line):
                novel_chapter = get_novel_chapter(trim_line)
                index_h.write(novel_chapter+"\n")
                chapter_path = dir_path+"/"+ novel_chapter+".txt"
                print(chapter_path)
            else:
                chapter_h=open(chapter_path,'a+',encoding="utf-8")
                chapter_h.write(trim_line+"\n")
                chapter_h.close()
        except Exception as e:
            print(e)
    index_h.close()

def split_txt_novel_to_book_section_dicts(file_path):
    file_encoding = common_filer.get_file_encoding(file_path)
    novel_lines = common_filer.get_file_details_by_encoding(file_path,file_encoding)
    section_dict = dict()
    section_list = []
    for novel_line in novel_lines:
        novel_chapter="序"
        trim_line = novel_line.strip().replace("\\","").replace("\r","").replace("）",")").replace("（","(")
        if is_novel_title(trim_line):
            novel_chapter = get_novel_chapter(trim_line)
            section_dict[novel_chapter]=""
        else:
            if novel_chapter in section_dict:
                section_dict[novel_chapter]=section_dict[novel_chapter]+trim_line+"\n"
            else:
                section_dict[novel_chapter]=trim_line+"\n"
    section_no = 0
    for section_key,section_val in section_dict.items():
        book_section_dict={"BookId":-1,"OrderNo":0,"SectionNo":section_no,"ChapterName":section_key,"Content":section_val}
        section_list.append(book_section_dict)
        section_no = section_no +1
    return section_list

def split_pdf_file_to_book_section_dicts(file_path):
    pdf_reader = SimplePdfReader(file_path)
    
    

def recur_split_novels_in_novel_parent_dir(dir_path):
    file_list = common_filer.get_child_absolute_files(dir_path)
    for file_path in file_list:
        if file_path.endswith(".txt"):
            split_txt_novel_to_chapter(file_path)

def recur_hider_files(dir_path,parent_dir,media_type):
    correct_dir = dir_path+"//"+parent_dir
    file_list = common_filer.get_child_absolute_files(correct_dir)
    map_list = []
    if common_filer.exists(dir_path + "//index.txt"):
        index_file_r = SimpleFileReader(dir_path + "//index.txt")
        for val in index_file_r.read_lines():
            map_list.append(val.replace("\n","")) 
    index_file_w = SimpleFileWriter(dir_path + "//index.txt")
    media_sql_file_w = SimpleFileWriter(dir_path + "//MediaData.sql")
    media_section_sql_file_w = SimpleFileWriter(dir_path + "//MediaSectionData.sql")
    
    start_id = 50000+len(map_list)
    for file_path in file_list:
        start_id = start_id +1
        start_id_str = str(start_id)
        if media_type == "video":
            if file_path not in map_list:
                print(file_path)
                index_file_w.append_new_line(file_path)
                file_size = common_filer.get_file_size(file_path)
                file_name = common_filer.get_file_name(file_path)
                file_media_name = file_name.replace(".mp4","")
                media_sql_str = "insert into Media values ("+start_id_str+",'"+file_media_name+"','/vhider/Video/亚洲无码','','','/img/novel_bg.jpg',3001,7200,"+str(file_size)+",now(),'alvin',0,'alvin',curdate());"
                media_section_sql_str = "insert into MediaSection(MediaId,OrderNo,SectionNo,Preffix,Time,Size,UpdateTime,UpdateUser,DeleteFlag,submission_user,submission_date) values("+start_id_str+",0,0,'mp4',7200,"+str(file_size)+",now(),'alvin',0,'alvin',curdate());"
                media_sql_file_w.append_new_line(media_sql_str)
                media_section_sql_file_w.append_new_line(media_section_sql_str)
            else:
                print("match:"+file_path)
        elif media_type == "image":
            if file_path not in map_list:
                print(file_path)
                index_file_w.append_new_line(file_path)
                file_name = common_filer.get_file_name(file_path)
                media_sql_str = "insert into Media values ("+start_id_str+",'"+file_name+"','/vhider/Image/漫画','','','/img/novel_bg.jpg',3016,7200,0,now(),'alvin',0,'alvin',curdate());"
                media_sql_file_w.append_new_line(media_sql_str)
                child_files = common_filer.get_child_files(file_path)
                child_files.sort()
                for child_id, child_file in enumerate(child_files):
                    child_idx = child_id +1
                    child_file_infos = child_file.split(".")
                    child_file_prefix= child_file_infos[-1]
                    child_correct_file = file_name+"_"+str(child_idx)+"."+child_file_prefix
                    print(child_file)
                    if child_correct_file not in child_files:
                        print(child_correct_file)
                        common_filer.move_file(file_path+"/"+child_file, file_path+"/"+child_correct_file)
                    media_section_sql_str = "insert into MediaSection(MediaId,OrderNo,SectionNo,Preffix,Time,Size,UpdateTime,UpdateUser,DeleteFlag,submission_user,submission_date) values("+start_id_str+","+str(child_idx)+",0,'"+child_file_prefix+"',7200,0,now(),'alvin',0,'alvin',curdate());"
                    media_section_sql_file_w.append_new_line(media_section_sql_str)
            else:
                print("match:"+file_path)
                
def rename_files(dir_path,parent_dir):
    correct_dir = dir_path+"//"+parent_dir
    file_list = common_filer.get_child_absolute_files(correct_dir)
    for file_path in file_list:
        file_name = common_filer.get_file_name(file_path)
        child_files = common_filer.get_child_files(file_path)
        child_correct_file = file_name+"_0.jpg"
        child_correct_file1 = file_name +"_0.png"
        if child_correct_file in child_files or child_correct_file1 in child_files:
            for child_id in range(len(child_files)-1,-1,-1):
                child_idx = child_id+1
                child_file = file_name+"_"+str(child_id)+".jpg"
                child_file1 = file_name+"_"+str(child_id)+".png"
                if child_file in child_files :
                    correct_file_name = file_name+"_"+str(child_idx)+".jpg"
                    print(file_path+"/"+child_file+","+file_path+"/"+correct_file_name)
                    
                    common_filer.move_file(file_path+"/"+child_file, file_path+"/"+correct_file_name)
                elif child_file1 in child_files:
                    correct_file_name1 = file_name+"_"+str(child_idx)+".png"
                    print(file_path+"/"+child_file1+","+file_path+"/"+correct_file_name1)
                    common_filer.move_file(file_path+"/"+child_file1, file_path+"/"+correct_file_name1)


def rename_child_files(dir_path):
    file_list = common_filer.get_child_absolute_files(dir_path)
    for child_file in file_list:
        print(child_file+","+child_file.replace("'",""))
        common_filer.move_file(child_file, child_file.replace("'",""))

if __name__ == "__main__":
#     recur_split_novels_in_novel_parent_dir("Y://小说//仙幻")
#     recur_hider_files("Y://Spider//Hider","Video//亚洲无码","video")
#     recur_hider_files("Y://Spider//Hider","Image//漫画","image")
#     rename_files("Y://Spider//Hider","Image//漫画")
#     rename_child_files("Y://Spider//Hider//Image//漫画//[漫画][渣渣汉化组][柚木N]姉恋")
    