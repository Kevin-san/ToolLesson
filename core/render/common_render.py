# -*- coding: UTF-8 -*-
'''
Created on 2019/6/1

@author: xcKev
'''

import tools.common_tools as commons

def render_template(template_file,dict_values):
    temp_hl=open(template_file,'r')
    temp_string=temp_hl.read()
    templates=temp_string.split('\n\n\n')
    all_keys=get_keys(templates,"#")
    loop_blocks=get_keys(templates, "`")
    loop_keys=get_loop_keys(loop_blocks)
    singleton_keys=list(set(all_keys)).difference(set(loop_keys))
    return_string=temp_string
    for sglt_key in singleton_keys:
        return_string=replace_by_key_value(return_string, sglt_key, dict_values[sglt_key.upper()])
    loop_dicts=get_loop_dicts(loop_blocks, loop_keys)
    for lp_blck,lp_keys in loop_dicts.items():
        lp_blcks = get_final_lp_blcks(lp_blck, lp_keys, dict_values)
        new_lp_blcks = get_lp_blcks(lp_blcks, lp_keys, dict_values, 0)
        return_string = replace_by_key_values(return_string, lp_blck, new_lp_blcks)
    return return_string

def get_lp_blcks(lp_blcks,lp_keys,dict_values,cnt_id):
    new_blcks=[]
    if cnt_id >= len(lp_keys):
        return lp_blcks
    for index,lp_blck in enumerate(lp_blcks):
        lp_key=lp_keys[cnt_id]
        rest_str=replace_by_key_value(lp_blck, lp_key, dict_values[lp_key.upper()][index])
        new_blcks.append(rest_str)
    cnt_id = cnt_id+1
    return get_lp_blcks(new_blcks, lp_keys, dict_values, cnt_id)

def get_final_lp_blcks(lp_blck,lp_keys,dict_values):
    len_list=get_loop_lens(lp_keys, dict_values)
    return get_duplicate_lp_blcks(lp_blck, len_list)

def get_duplicate_lp_blcks(lp_blck,len_lst):
    blck_length=0
    if len(len_lst) ==1:
        blck_length=int(len_lst[0])
    return [lp_blck]*blck_length

def get_loop_lens(lp_keys,dict_values):
    len_list=[]
    for lp_key in lp_keys:
        len_list.append(len(dict_values[lp_key]))
    return list(set(len_list))

def get_loop_dicts(loop_blocks,loop_keys):
    loop_dict=dict()
    for lp_block in loop_blocks:
        sub_lp_keys=[]
        for lp_key in loop_keys:
            if '#%s#' %(lp_key) in lp_block:
                sub_lp_keys.append(lp_key)
        loop_dict[lp_block]=sub_lp_keys
    return loop_dict

def replace_by_key_value(temp_str,dict_key,dict_value):
    return temp_str.repalce('#%s#' %(dict_key),str(dict_value))

def replace_by_key_values(temp_str,dict_key,dict_vals):
    return temp_str.replace('`%s`' %(dict_key),'\n'.join(dict_vals))

def get_keys(templates,key_str):
    unique_keys=set()
    for temp_str in templates:
        all_ids=commons.get_all_ids(temp_str, key_str)
        end=int(len(all_ids)/2)
        for index in range(0,end):
            start_id=all_ids[2*index]+1
            end_id=all_ids[2*index+1]
            if '' != temp_str[start_id:end_id]:
                unique_keys.add(temp_str[start_id:end_id])
    return list(unique_keys)

def get_loop_keys(key_list):
    new_set=set()
    uq_keys=get_keys(key_list,'#')
    new_set=new_set.union(uq_keys)
    return list(new_set)
