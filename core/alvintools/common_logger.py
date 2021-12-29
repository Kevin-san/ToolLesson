#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/1

@author: xcKev
'''

import logging

import os
from alvintools import common_dater
dater = common_dater.DateConverter(common_dater.holiy_file)
LOG_DIR='/temp'

def get_log(log_name,log_filedir,logger_name,level=logging.INFO):
    time_str = dater.date2str(dater.today(), "%Y_%m_%d")
    logname = F"{log_name}.{time_str}.log"
    if not os.path.isdir(log_filedir):
        print(F"{log_filedir} not exist,start create log dir")
        os.mkdir(log_filedir)
    else:
        print(F"log dir {log_filedir} exist")
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')
    file_handler = get_file_handler(formatter,F"{log_filedir}/{logname}")
    clean_logs(F"{log_filedir}/{logname}",30)
    file_handler.setLevel(level)
    console_handler = get_console_handler(formatter)
    console_handler.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def get_console_handler(log_formatter):
    console_handler=logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    return console_handler

def get_file_handler(log_formatter,file_name):
    file_handler=logging.FileHandler(file_name)
    file_handler.setFormatter(log_formatter)
    return file_handler

def clean_logs(path,days):
    if os.path.exists(path) and os.path.isdir(path):
        calc_dates = dater.calculate_dates(days,"%Y_%m_%d")
        for file in os.listdir(path): #os.listdir(path) 文件夹下所有文件名字，存在list里
            file_name_sp = file.split('.')# 日志名字按.分割，分割成['catalina', '2017-06-13', 'log']
            if len(file_name_sp)>2 :# 日志名字中有不带日期的，需要过滤掉,过滤掉['catalina','out']['c_']这两个文件
                file_date = file_name_sp[1]
                if file_date not in calc_dates:
                    abs_path = os.path.join(path,file)
                    print('已删除：%s'%abs_path)
                    os.remove(abs_path)
        else:
            print('没有可删除的文件')
    else:
        print('路径不存在或者不是一个目录')