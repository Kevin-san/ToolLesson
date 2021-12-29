#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/30

@author: xcKev
'''

import json
import re
import sqlparse
import alvintools.common_converter as converter
from bs4 import BeautifulSoup
from htmlmin.minify import html_minify
from rjsmin import jsmin
from rcssmin import cssmin
from xml.dom import minidom
import jsbeautifier

def format_json(json_str):
    dic = converter.json_to_dict(json_str)
    format_js = json.dumps(dic,indent=4,separators=(',',':'))
    return format_js

def format_json_esc(json_str):
    dic = converter.json_to_dict(json_str)
    format_js = json.dumps(dic,sort_keys=True,indent=4,separators=(',',':'))
    return format_js

def format_json_desc(json_str):
    dic = converter.json_to_dict(json_str)
    dic_list = list(dic.items())
    dic_list.sort(reverse=True)
    format_js = json.dumps(dict(dic_list),sort_keys=False,indent=4,separators=(',',':'))
    return format_js

def trans_json(json_str):
    trans_json_str=json.dumps(json_str)
    return trans_json_str[1:-1]

def re_trans_json(json_str):
    trans_json_str=json_str.replace('\\"','"')
    return json.dumps(json.loads(trans_json_str),indent=4,separators=(',',':'))

def format_js(js_str):
    return jsbeautifier.beautify(js_str)

def format_sql(sql_str):
    stmts=sqlparse.split(sql_str)
    sql_strs=[]
    for stmt in stmts:
        sql_strs.append(sqlparse.format(stmt, reindent=True, keyword_case='upper'))
    return "\n".join(sql_strs)

def format_html(html_str):
    html=BeautifulSoup(html_str,'html5lib')
    return html.prettify()

def format_xml(xml_str):
    reparsed=minidom.parseString(compress_xml(xml_str))
    return reparsed.toprettyxml(indent='\t')

def format_css(css_str):
    return css_str.replace("{","{\n\t").replace("}","\n}\n").replace(";",";\n\t")

def compress_str(format_str):
    str_list=re.split(r'\s+(?=[^"]*(?:"[^"]*"[^"]*)*$)|\s+(?=[^\']*(?:\'[^\']*\'[^\']*)*$)',format_str)
    return " ".join(str_list)

def compress_js(js_str):
    return jsmin(js_str, keep_bang_comments=True)

def compress_json(json_str):
    dic = converter.json_to_dict(json_str)
    return converter.dict_to_json(dic)

def compress_sql(sql_str):
    sql_strs=[]
    for sql_item in sql_str.split('\n'):
        comments = sql_item.split('--');
        if len(comments) >1:
            sql_strs.append(compress_str(sql_item)+'\n')
        else:
            sql_strs.append(compress_str(sql_item))
    return "".join(sql_strs)

def compress_html(html_str):
    return html_minify(html_str)

def compress_xml(xml_str):
    return html_minify(xml_str,parser='xml')

def compress_css(css_str):
    return cssmin(css_str,keep_bang_comments=False)



