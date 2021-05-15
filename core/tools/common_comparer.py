#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/30

@author: xcKev
'''

import difflib
import tools.common_filer as filer
import tools.common_logger as log
import sys
current_log=log.get_log('comparer', log.LOG_DIR, 'comparer')

def compare_file(file_path1,file_path2,diff_path):
    if file_path1 == "" or file_path2 =="":
        current_log.info(F"path can't be blank: first path:{file_path1},second path:{file_path2}")
        sys.exit()
    else:
        current_log.info(F"comparing file between {file_path1} and {file_path2}")
    text1_lines = filer.get_file_details(file_path1)
    text2_lines = filer.get_file_details(file_path2)
    diff = difflib.HtmlDiff()
    result = diff.make_file(text1_lines, text2_lines)
    try:
        result_h = open(diff_path,'w')
        result_h.write(result)
        current_log.info("Compared successfully finished\n")
    except IOError as error:
        current_log.error(F"Failed to write html diff file: {error}")