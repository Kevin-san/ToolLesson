#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/1

@author: xcKev
'''

import logging

import os
import time

def get_log(log_name,log_filedir,logger_name,level=logging.INFO):
    time_str = time.strftime("%Y_%m_%d", time.localtime(time.time()))
    logname = F"{time_str}_{log_name}.log"
    if not os.path.isdir(log_filedir):
        print(F"{log_filedir} not exist,start create log dir")
        os.mkdir(log_filedir)
    else:
        print(F"log dir {log_filedir} exist")
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineNo)d - %(message)s')
    file_handler = get_file_handler(formatter,F"{log_filedir}/{logname}")
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
    