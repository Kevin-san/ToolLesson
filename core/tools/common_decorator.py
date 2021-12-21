#-*- encoding:UTF-8 -*-
'''
Created on 2021/12/18

@author: xcKev
'''
import tools.common_logger as log
current_log=log.get_log('sql_output', log.LOG_DIR, 'sql_output')

def sql_output(func):
    def inner_sql_output(sql_str,*args,**kwargs):
        try:
            current_log.info(sql_str)
            return func(sql_str,*args,**kwargs)
        except Exception as e:
            current_log.error('Error execute: %s' % func.__name__ )
            current_log.error(e)
    return inner_sql_output