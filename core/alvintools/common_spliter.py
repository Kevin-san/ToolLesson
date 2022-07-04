#-*- encoding:UTF-8 -*-
'''
Created on 2021/7/11

@author: xcKev
'''
from alvintools import common_filer,common_tools
import alvintools
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
        if common_tools.is_novel_chapter(line_str):
            return True
    return False

def get_novel_chapter(trim_line):
    line_list = split_chapter_names(trim_line)
    for line_id,line_str in enumerate(line_list):
        if common_tools.is_novel_chapter(line_str):
            return " ".join(line_list[line_id:]).replace("?","").replace("：","").replace(" ","")

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
    pdf_folder = file_path.replace(file_path,".pdf")
    file_name = common_filer.get_file_name(file_path)
    img_parent_folder=alvintools.get_remote_folder()+"/图片"
    img_folder=alvintools.get_remote_folder()+"/图片/learn/"+file_name
    common_filer.make_dirs(img_folder)
    common_filer.make_dirs(pdf_folder)
    pdf_reader = SimplePdfReader(file_path)
    page_cnt=pdf_reader.get_page_cnt()
    section_list=[]
    menu_len = len(pdf_reader.menus)
    for menu_id, menu in enumerate(pdf_reader.menus):
        menu_title = menu[1]
        menu_start = menu[2]-1
        if menu_id == menu_len -1:
            menu_end = page_cnt
        else:
            menu_end = pdf_reader.menus[menu_id+1][2]-2
        section_contents=[]
        for i in range(menu_start,menu_end):
            page_real_index = i+1
            convert_file_name=F"{img_folder}/{page_real_index}"
            for item_id, item in enumerate(pdf_reader.extract_dict_to_items(i)):
                if common_tools.is_list(item):
                    for it in item:
                        section_contents.append(common_tools.output_str_from_item(it, convert_file_name, img_parent_folder, item_id, ""))
                else:
                    section_contents.append(common_tools.output_str_from_item(item, convert_file_name, img_parent_folder, item_id, "\n"))
        book_section_dict={"BookId":-1,"OrderNo":0,"SectionNo":menu_id,"ChapterName":menu_title,"Content":"".join(section_contents)}
        section_list.append(book_section_dict)
    return section_list
    

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
        
        if media_type == "video":
            if file_path not in map_list:
                start_id = start_id +1
                start_id_str = str(start_id)
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
                start_id = start_id +1
                start_id_str = str(start_id)
                print(file_path)
                index_file_w.append_new_line(file_path)
                file_name = common_filer.get_file_name(file_path)
                media_sql_str = "insert into Media values ("+start_id_str+",'"+file_name+"','/vhider/Image/漫画/"+file_name+"','','','/img/novel_bg.jpg',3016,7200,0,now(),'alvin',0,'alvin',curdate());"
                media_sql_file_w.append_new_line(media_sql_str)
                child_files = common_filer.get_child_files(file_path)
                child_files.sort()
                for child_id, child_file in enumerate(child_files):
                    child_file_infos = child_file.split(".")
                    child_file_prefix= child_file_infos[-1]
                    child_correct_file = file_name+"_"+str(child_id)+"."+child_file_prefix
                    print(child_file)
                    if child_correct_file not in child_files:
                        print(child_correct_file)
                        common_filer.move_file(file_path+"/"+child_file, file_path+"/"+child_correct_file)
                    media_section_sql_str = "insert into MediaSection(MediaId,OrderNo,SectionNo,Preffix,Time,Size,UpdateTime,UpdateUser,DeleteFlag,submission_user,submission_date) values("+start_id_str+","+str(child_id)+",0,'"+child_file_prefix+"',7200,0,now(),'alvin',0,'alvin',curdate());"
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
        child_correct_file2 = file_name + "_0.PNG"
        if child_correct_file not in child_files and child_correct_file1 not in child_files and child_correct_file2 not in child_files:
            for child_id in range(1,len(child_files)+1):
                child_idx = child_id-1
                child_file = file_name+"_"+str(child_id)+".jpg"
                child_file1 = file_name+"_"+str(child_id)+".png"
                child_file2 = file_name+"_"+str(child_id)+".PNG"
                if child_file in child_files :
                    correct_file_name = file_name+"_"+str(child_idx)+".jpg"
                    print(file_path+"/"+child_file+","+file_path+"/"+correct_file_name)
                    
                    common_filer.move_file(file_path+"/"+child_file, file_path+"/"+correct_file_name)
                elif child_file1 in child_files:
                    correct_file_name1 = file_name+"_"+str(child_idx)+".png"
                    print(file_path+"/"+child_file1+","+file_path+"/"+correct_file_name1)
                    common_filer.move_file(file_path+"/"+child_file1, file_path+"/"+correct_file_name1)
                elif child_file2 in child_files:
                    correct_file_name1 = file_name+"_"+str(child_idx)+".png"
                    print(file_path+"/"+child_file2+","+file_path+"/"+correct_file_name1)
                    common_filer.move_file(file_path+"/"+child_file2, file_path+"/"+correct_file_name1)


def rename_child_files(dir_path):
    file_list = common_filer.get_child_absolute_files(dir_path)
    for child_file in file_list:
        print(child_file+","+child_file.replace("'",""))
        common_filer.move_file(child_file, child_file.replace("'",""))

def rename_child_files_by_spec_list(dir_path,dir_name_list):
    for dir_name in dir_name_list:
        real_dir = dir_path+"/"+dir_name
        files = common_filer.get_child_absolute_files(real_dir)
        file_idxs=[]
        for file_name in files:
            file_idx = file_name.split("_")[-1].split(".")[0]
            file_idxs.append(int(file_idx))
        file_idxs.sort()
        for list_id,list_val in enumerate(file_idxs):
            correct_file_name1 = real_dir+"/"+dir_name+"_"+str(list_id)+".jpg"
            child_file = real_dir+"/"+dir_name+"_"+str(list_val)+".jpg"
            print(child_file+","+correct_file_name1)
            common_filer.move_file(child_file, correct_file_name1)

if __name__ == "__main__":
#     recur_split_novels_in_novel_parent_dir("Y://小说//仙幻")
#     recur_hider_files("Y://Spider//Hider","Video//亚洲无码","video")
#     recur_hider_files("Y://Spider//Hider","Image//漫画","image")
    book_section_dicts=split_pdf_file_to_book_section_dicts("E:/IDE/allpdf/allpdf/textpdf/Python核心编程.pdf")
    for dict_book in book_section_dicts:
        print(dict_book)
#     rename_files("Y://Spider//Hider","Image//漫画")
#     dir_name_list = ['[きひる]我的后宫佳丽_僕のハーレム[风的工房] [176p]',
# '[ゲンツキ] 偏爱ヒロイズム [高画质][无邪気汉化组X无毒汉化组] [202p]',
# '[ポン贵花田] とろとろえっち [204p]',
# '[武内一真]とらいあんぐるH[光年汉化组] [203p]',
# '[武田あらのぶ]ヒメハメトリップ[ROC_1112高清扫图] [215p]',
# '[武田弘光]いまりあ[空気系☆汉化] [218p]',
# '[泽野明] 兄想う故に妹あり 限定版 [209p]',
# '[泽野明] 妹と付き合う11の方法 [206p]',
# '[美矢火] 美少女公主_オトメヒメ [无邪気汉化组][MJK-15-D100] [207p]',
# '[英丸] ハッスル! 団地妻[中国翻訳][魔剑个人汉化]',
# '[蓬瑠璃] ハジメテのヒト [200p]',
# '[锦ヶ浦鲤三郎] ほっこり桃源郷 [101p]',
# '[高津]妖魔淫宴与爆乳肉慾性活 [219p]']
# 
#     rename_child_files_by_spec_list("Y:/Spider/Hider/Image/漫画", dir_name_list)
        
# 1. rename files 2. insert data 3. update data 4. soft link
#     rename_child_files("Y://Spider//Hider//Image//漫画//[漫画][渣渣汉化组][柚木N]姉恋")