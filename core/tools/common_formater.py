#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/30

@author: xcKev
'''

import json
import re
from re.RegexFlag import IGNORECASE
from deps import sql_format
import tools.common_converter as converter
import tools.common_tools as common

def format_js(js_str):
    lines = js_str.split(";")
    indent = 0
    formatted = []
    for line in lines:
        newline = []
        for char in line:
            newline.append(char)
            if char=='{':
                indent+=1
                newline.append("\n")
                newline.append("\t"*indent)
            if char=='}':
                indent-=1
                newline.append("\n")
                newline.append("\t"*indent)
        formatted.append("\t"*indent+"".join(newline))
    return ";\n".join(formatted)

def format_json(json_str):
    dic = converter.json_to_dict(json_str)
    format_js = json.dumps(dic,sort_keys=True,indent=4,separators=(',',':'))
    return format_js

def format_sql(sql_str):
    return sql_format(sql_str, wrap_add=None, mode='upper')

def format_xml(xml_str):
    new_xml_list=""
    xml_list = re.split(r'([>])',xml_str)
    xml_list = ["".join(i) for i in zip(xml_list[0::2],xml_list[1::2])]
    level=0
    for node in xml_list:
        if re.match(r'<\?xml .*version.*\?>', node):
            new_xml_list=new_xml_list+node
            continue
        elif re.match(r'<[^\?^/].*[^/]>', node):
            new_xml_list=new_xml_list+common.get_space(level)+node
            level=level+1
            continue
        elif re.match(r'</.*[^/]>', node):
            level=level-1
            new_xml_list=new_xml_list+common.get_space(level)+node
            continue
        elif re.match(r'<[^/].*/>',node):
            new_xml_list=new_xml_list+common.get_space(level)+node
        elif re.match(r'.+</.*[^/]>',node):
            new_xml_list=new_xml_list+node
            level=level-1
        else:
            new_xml_list=new_xml_list+node
    return new_xml_list

def format_css(css_str):
    return css_str.replace("{","{\n\t").replace("}","\n}\n").replace(";",";\n\t")

def compress_json(json_str):
    dic = converter.json_to_dict(json_str)
    return converter.dict_to_json(dic)

def compress_sql(sql_str):
    next_str=' '.join(sql_str.split('\n')).replace('    ','')
    return re.sub(r"\s{2,}"," ",next_str)

def compress_xml(xml_str):
    next_str=' '.join(xml_str.split('\n')).replace('    ','').replace('> ','>').replace(' <','<')
    return re.sub(r"\s{2,}"," ",next_str)

def compress_css(css_str):
    css_str=re.sub(r"\n\t+","",css_str)
    css_str=css_str.replace("\n","")
    ignore_pattern=re.compile(r'\s*\:\s*', IGNORECASE)
    css_str=ignore_pattern.sub(':',css_str)
    ignore_pattern=re.compile(r';?\s*\}\s*', IGNORECASE)
    css_str=ignore_pattern.sub('}',css_str)
    ignore_pattern=re.compile(r'\s*\{\s*', IGNORECASE)
    css_str=ignore_pattern.sub('{',css_str)
    ignore_pattern=re.compile(r'\s{2,}', IGNORECASE)
    css_str=ignore_pattern.sub(' ',css_str)
    ignore_pattern=re.compile(r'/\*[\s\S]*?\*/', IGNORECASE)
    css_str=ignore_pattern.sub('',css_str)
    return css_str
