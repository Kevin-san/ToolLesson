#-*- encoding:UTF-8 -*-
'''
Created on 2019/11/30

@author: xcKev
'''
import decimal
import unicodedata
import alvintools.common_converter as converter
import alvintools.common_logger as log
import alvinconst.javatmps as javatmps
from alvinconst.filesuffixs import FileSuffix
from alvintools import common_converter
import time
import re

filesuffix=FileSuffix()

java_cons=javatmps.JavaConst()
suffix_names=filesuffix.file_suffix_names + filesuffix.compiled_suffix_names+filesuffix.config_suffix_names+filesuffix.html_suffix_names+filesuffix.img_suffix_names+filesuffix.video_suffix_names+filesuffix.msc_suffix_names+filesuffix.package_suffix_names+filesuffix.run_suffix_names
current_log=log.get_log('alvintools', '/temp', 'alvintools')

def get_val_max(num_list):
    max_val = max(num_list)
    if max_val > 100:
        return 1000
    elif max_val <10 and max_val >0:
        return 10
    return 100

def get_max_length(cols):
    max_length_col = max(cols)
    return len(max_length_col)

def get_max_length_col_from_table(table_list):
    reverse_tables=[[row[i] for row in table_list] for i in range(len(table_list[0]))]
    max_cols_list = []
    for cols in reverse_tables:
        max_cols_list.append(cols)
    return get_max_length(max_cols_list)

def convert_common_rules_to_tag_dict(rule_list):
    tag_dict=dict()
    for common_rule in rule_list:
        tag_dict[common_rule.TypeVal]=common_rule
    return tag_dict

def get_correct_vals_by_cols_num(cols_num,text_val):
    text_val=text_val.replace("\r\n","")
    text_length = len(text_val)
    correct_vals = []
    line_cnt = int(text_length / cols_num)
    if text_length % cols_num != 0:
        line_cnt=line_cnt+1
    for index in range(0,line_cnt):
        begin_index= index*cols_num
        end_index=(index+1)*cols_num
        if end_index >= text_length:
            end_index = text_length
        correct_vals.append(text_val[begin_index:end_index])
    return correct_vals

def obj_to_string(cls, obj):
    """
          简单地实现类似对象打印的方法
    :param cls: 对应的类(如果是继承的类也没有关系，比如A(object), cls参数传object一样适用，如果你不想这样，可以修改第一个if)
    :param obj: 对应类的实例
    :return: 实例对象的to_string
    """
    if not isinstance(obj, cls):
        raise TypeError("obj_to_string func: 'the object is not an instance of the specify class.'")
    to_string = str(cls.__name__) + "("
    items = obj.__dict__
    n = 0
    for k in items:
        if k.startswith("_"):
            continue
        to_string = to_string + str(k) + "=" + str(items[k]) + ","
        n += 1
    if n == 0:
        to_string += str(cls.__name__).lower() + ": 'Instantiated objects have no property values'"
    return to_string.rstrip(",") + ")"

def create_map(keylist,valuelist):
    return dict(zip(keylist,valuelist))

def group_by_list(func,item,group_dicts):
    par_key = func(item)
    if par_key in group_dicts:
        group_dicts[par_key].append(item)
    else:
        group_dicts[par_key]=[]

def group_by_str(func,item,group_dicts):
    par_key = func(item)
    current_str=str(item)
    if par_key in group_dicts:
        last_str = group_dicts[par_key]
        group_dicts[par_key] = F"{last_str}{current_str}"
    else:
        group_dicts[par_key] = F"{current_str}"

def group_detail_by_dist_parent_key(func1,func2,children_details):
    group_dicts={}
    for child_det in children_details:
        func1(func2,child_det,group_dicts)
    return group_dicts

def check_obj_type(py_object,class_type):
    if isinstance(py_object, class_type):
        return True
    else:
        return False

def is_base_object(obj_val):
    return is_str(obj_val) or is_int(obj_val) or is_float(obj_val) or is_bool(obj_val)

def is_int(obj_val):
    try:
        obj_val = int(obj_val)
    except Exception:
        return False
    return check_obj_type(obj_val, int)

def is_bool(obj_val):
    return check_obj_type(obj_val, bool)

def is_str(obj_val):
    return check_obj_type(obj_val, str)

def is_time(obj_val):
    if is_str(obj_val):
        try:
            date_strs=re.findall(":",obj_val)
            if len(date_strs) >=2 :
                time.strptime(obj_val,"%Y-%m-%d %H:%M:%S")
            elif 0 < len(date_strs) < 2:
                time.strptime(obj_val,"%Y-%m-%d %H:%M")
            else:
                time.strptime(obj_val,"%Y-%m-%d")
            return True
        except Exception:
            return False
    return False

def is_float(obj_val):
    return check_obj_type(obj_val, float)
def is_dict(dict_obj):
    return check_obj_type(dict_obj, dict)

def is_list(list_obj):
    return check_obj_type(list_obj, list)

def is_tuple(tuple_obj):
    return check_obj_type(tuple_obj, tuple)

def is_set(set_obj):
    return check_obj_type(set_obj, set)

def is_number(obj_val):
    try:
        float(obj_val)
        return True
    except ValueError:
        pass
    try:
        unicodedata.numeric(obj_val)
    except (TypeError,ValueError):
        pass
    return False

def is_http_url(href_url):
    return href_url.startswith('http://') or href_url.startswith('https://')

def is_file(str_name_list):
    for str_name in str_name_list:
        str_arrs=str_name.split('.')
        if str_arrs[-1] not in suffix_names:
            return False
    return True

def is_blank(check_val):
    return check_val is None or check_val ==''

def is_list_and_ge_len(object_item,length):
    return isinstance(object_item,list) and len(object_item) >=length

def to_normalize(param_str):
    return param_str[:1].upper()+param_str[1:]

def to_integer_list(param_array):
    param_list=[]
    for i in range(len(param_array)):
        param_list.append(int(param_array[i]))
    return param_list

def to_unique_list(param_list):
    new_param_list=list(set(param_list))
    new_param_list.sort(key=list(param_list).index)
    return new_param_list

def get_filter_list_baseon_list(target_list,source_list):
    if source_list:
        return sorted(set(target_list).difference(set(source_list)),key=target_list.index)
    return target_list

def to_template_str(str_template,val_list):
    val_tuple=tuple(val_list)
    return str_template %val_tuple

def to_single_template_str(val_list):
    str_template = '%s'*len(val_list)
    val_tuple = tuple(val_list)
    return str_template %val_tuple

def to_thousands_format(val_num):
    return format(val_num,',')

def get_dict_key(dict_keys,csv_id):
    if csv_id >= len(dict_keys):
        key ="undefined"
    else:
        key=dict_keys[csv_id]
    return key

def get_lower_num(num1,num2):
    return num1 if num1 < num2 else num2

def get_bigger_num(num1,num2):
    return num1 if num1 > num2 else num2

def get_correct_str(val_obj):
    if is_str(val_obj):
        return '"'+str(val_obj)+'"'
    return str(val_obj)

def get_bool_correct_str(val_obj):
    bool_correct_str= ''
    if is_bool(val_obj):
        bool_correct_str='true' if val_obj else 'false'
    else:
        bool_correct_str=get_correct_str(val_obj)
    return bool_correct_str

def get_sorted_keys(dict_obj,reverse_flag):
    return sorted(dict_obj,reverse=reverse_flag)

def get_space(level):
    space='\n'
    space = space + '    '*level
    return space

def get_home_path(url_path):
    if url_path.endswith('.html'):
        return url_path
    if url_path[-1]!='/':
        url_path=url_path+'/'
    return url_path

def is_single_list(list_vals):
    for list_v in list_vals:
        if is_complex_item(list_v):
            return False
    return True

def is_complex_item(item_val):
    return is_list(item_val) or is_dict(item_val)

def find_vals_from_dict_by_keystr(complex_dict,key_str,result_vals):
    get_dict_vals(complex_dict, key_str, result_vals)
    current_log.info(result_vals)
    return result_vals

def get_upload_path(parent_folder,media_type):
    upload_map={"video":"视频","audio":"音频","image":"图片","learn":"学习","novel":"小说"}
    return parent_folder+"/"+upload_map[media_type]

def get_list_vals(values,key_str,result_vals):
    for val in values:
        if is_str(val) and val.find(key_str)!=-1:
            result_vals.append(val)
        if is_list(val):
            get_list_vals(val,key_str,result_vals)
        elif is_dict(val):
            get_dict_vals(val, key_str, result_vals)

def get_dict_vals(valdics,key_str,result_vals):
    for val in valdics.values():
        if is_str(val) and val.find(key_str)!=-1:
            result_vals.append(val)
        if is_list(val):
            get_list_vals(val, key_str,result_vals)
        elif is_dict(val):
            get_dict_vals(val, key_str, result_vals)

def get_dir_file(name_path):
    file_arrs=name_path.split('.')
    new_file_arrs=file_arrs[:-1]
    file_name=file_arrs[-1]
    dir_name='/'.join(new_file_arrs)
    return dir_name,file_name

def get_directory_file_list(name_list):
    dir_list=[]
    file_list=[]
    for name_path in name_list:
        dir_name,file_name=get_dir_file(name_path)
        dir_list.append(dir_name)
        file_list.append(file_name)
    return dir_list,file_list

def get_csv_headers(csv_list,header_index,split_char):
    key_line = csv_list[0]
    if header_index > 0 and len(csv_list) > header_index:
        key_list = []
        for idx in range(0,header_index):
            key_list.append(csv_list[idx])
        key_line=split_char.join(key_list)
    return key_line.split(split_char)

def get_csv_str_from_dict(header_keys,split_char,item_dict):
    item_list=[]
    for key in header_keys:
        item_list.append(str(item_dict[key]))
    return split_char.join(item_list)

def get_dict_from_csv_str(header_keys,split_char,csv_str):
    csv_values=csv_str.split(split_char)
    json_dict={}
    for csv_id in range(0,len(csv_values)):
        key=get_dict_key(header_keys,csv_id)
        json_dict[key]=csv_values[csv_id]
    return json_dict

def get_spec_var(check_val,match_val,els_val):
    if is_blank(check_val):
        return match_val
    return els_val

def get_all_ids(src_str,target_str):
    all_ids=[]
    count=get_cnt_by_spec_str(src_str, target_str)
    for i in range(0,count):
        spec_id=get_index_of_str(src_str,target_str)
        lst_spec_id = spec_id
        if len(all_ids)>0:
            spec_id=spec_id+all_ids[i-1]+len(target_str)
        all_ids.append(spec_id)
        src_str=src_str[lst_spec_id+1:]
    return all_ids

def get_all_idx(src_str,target_str):
    all_idx=[]
    item_list=src_str.split(target_str)
    for idx,item in enumerate(item_list):
        if idx!=0:
            last_id=all_idx[idx-1]
            all_idx.append(last_id+len(item)+len(target_str))
        all_idx.append(len(item))
    return all_idx[:-1]

def get_index_of_str(src_str,target_str):
    return src_str.find(target_str)

def get_cnt_by_spec_str(src_str,target_str):
    temp_items=src_str.split(target_str)
    return len(temp_items)-1

def get_camel_id(param_str):
    id_list=[]
    for i in range(1,len(param_str)):
        if param_str[i].isupper() and param_str[i-1].islower():
            id_list.append(i)
    for i in range(0,len(param_str)-1):
        if param_str[i].isupper() and param_str[i+1].islower():
            id_list.append(i)
    id_list=to_unique_list(id_list)
    return id_list

def get_upper_char_id(param_str):
    id_list=[]
    for i in range(0,len(param_str)):
        if param_str[i].isupper():
            id_list.append(i)
    return id_list

def get_lower_char_id(param_str):
    id_list=[]
    for i in range(0,len(param_str)):
        if param_str[i].islower():
            id_list.append(i)
    return id_list

def del_dict_key(dict1,key):
    removed_val=dict1.pop(key,'not exist this key')
    return removed_val

def merge_dict(dict1,dict2):
    return (dict2.update(dict1))

def count_lst_item(lst,item):
    return lst.count(item)

def real_round(val_num,digit):
    val = decimal.Decimal(str(val_num))
    decimal.getcontext().rounding=decimal.ROUND_HALF_UP
    return round(val,digit)

def trim(str_val):
    return str_val.strip()

def discard(val_num,digit):
    return int(val_num*(10**digit))/(10**digit)

def raised(val_num,digit):
    val_discard=discard(val_num, digit)
    if val_discard==val_num:
        return val_discard
    magic=val_num>0 if 1 else -1
    return (val_discard+(magic/10**digit))

def add_char_to_str_last(val_str,char_str,char_len):
    last_str = char_str*char_len
    return val_str+last_str

def add_char_to_str_first(val_str,char_str,char_len):
    head_str = char_str*char_len
    return head_str+val_str

def add_char_to_str_both_side(val_str,char_str,char_len):
    added_head = add_char_to_str_first(val_str, char_str, char_len)
    return add_char_to_str_last(added_head, char_str, char_len)

def add_item_into_dict_val_by_key(val_dict,dict_key,val_item):
    if dict_key in val_dict.keys():
        val_dict[dict_key].append(val_item)
    else:
        val_dict[dict_key] = []
        val_dict[dict_key].append(val_item)

def replace_duplicate_str(dup_str,char_str):
    old_str=to_single_template_str([char_str,char_str])
    new_str=to_single_template_str([char_str])
    result_str=dup_str.replace(old_str,new_str)
    all_idx=get_all_idx(result_str, old_str)
    if len(all_idx)==0:
        return result_str
    return replace_duplicate_str(result_str, char_str)

def list_to_content_blck(property_list):
    param_list=[]
    for proper in property_list:
        temp_str=to_template_str(java_cons.THIS_VAL,[proper.property_name,proper.property_name])
        param_list.append(temp_str)
    return '\n'.join(param_list)

def list_to_param_str(property_list):
    param_list=[]
    for proper in property_list:
        temp_str=to_template_str(java_cons.PARAMETER,[proper.property_type,proper.property_name])
        param_list.append(temp_str)
    return ','.join(param_list)

def list_to_in_clause_sql(result_lines,is_string):
    if int(is_string)==1:
        for result_id,result_item in enumerate(result_lines):
            result_lines[result_id]="'%s'" %(result_item)
    return to_template_str("( %s )", [",".join(result_lines)])

def list_to_sort_str(val_list,org_str,reverse_flag):
    if len(val_list)!=0:
        val_list=get_sorted_keys(val_list,reverse_flag)
        return ','.join(val_list)
    return org_str

def to_camel_core(param_list):
    for (index,param) in enumerate(param_list):
        param_list[index]=common_converter.first_upper(param.replace(" ",""), 1)
    return "".join(param_list)

def to_camel(param_str):
    if type(param_str) == list:
        return to_camel_core(param_str)
    elif type(param_str) == str:
        return to_camel_core(param_str.replace(" ","").split("_"))
    else:
        return ""

def to_underscore_core(param_list):
    for (index,param) in enumerate(param_list):
        param_list[index]=param.replace(" ","").upper()
    return "_".join(param_list)

def to_underscore(param_str):
    if type(param_str) == list:
        return to_underscore_core(param_str)
    elif type(param_str) == str:
        new_param_str=param_str.replace(" ","")
        all_ids=get_camel_id(new_param_str)
        param_list=[]
        curor_id=0
        for index in all_ids:
            if index>0:
                param_list.append(new_param_str[curor_id:index])
                curor_id=index
        param_list.append(new_param_str[curor_id:len(new_param_str)])
        return to_underscore_core(param_list)
    else:
        return ""

def sort_json(json_str,reverse_flag):
    json_dic=converter.json_to_dict(json_str)
    return sorted_dict_to_str(json_dic,reverse_flag)

def sort_dict(dict_obj,reverse_flag):
    result = ''
    if dict_obj is None:
        return result
    if is_base_object(dict_obj):
        result += get_bool_correct_str(dict_obj)+','
    if is_dict(dict_obj):
        sorted_list = get_sorted_keys(dict_obj, reverse_flag)
        for sorted_item in sorted_list:
            result += get_correct_str(sorted_item) +':'+sort_dict(dict_obj[sorted_item], reverse_flag)
        result='{'+result[:-1]+'}'
    if is_list(dict_obj):
        val_list=[]
        for t in dict_obj:
            if is_base_object(t):
                bool_correct_str = get_bool_correct_str(t)
                val_list.append(bool_correct_str)
            else:
                result+=sort_dict(t, reverse_flag)
        result='['+list_to_sort_str(val_list, result, reverse_flag)+']'
    result=replace_duplicate_str(result, ',')
    return result.replace('},]', '}]')

def sorted_dict_to_str(dict_obj,reverse_flag):
    sorted_str=sort_dict(dict_obj, reverse_flag)
    return sorted_str[:-1]

def group_format(obj_val):
    return format(obj_val, ',')

def get_count(str1,str2):
    return (len(str1) - len(str1.replace(str2,""))) // len(str2)


def is_novel_chapter(line_str):
    line_str = line_str.strip()
    match_obj = re.search(r'^第(\s*)([一二三四五六七八九十百千0123456789]*)(\s*)([章节回页]{1})(\s*)(.*)',line_str,re.M|re.I)
    if match_obj:
        print(line_str)
        return True
    return False

def output_str_from_item(item,convert_file_name,real_image_folder,index,break_str):
    if item.item_type == 'image':
        ext = item.ext
        image_file_path = F"{convert_file_name}_{index}.{ext}"
        current_log.info(image_file_path)
        file_w=open(image_file_path,'wb')
        file_w.write(item.imgdata)
        file_w.close()
        image_url = image_file_path.replace(real_image_folder,"/img")
        image_src=F"![alt {item.index}]({image_url}){break_str}"
        return image_src
    elif item.item_type == "link":
        return F"[{item.text}]({item.to_pageno}){break_str}"
    else:
        return item.text+break_str
