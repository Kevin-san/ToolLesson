#-*- encoding:UTF-8 -*-
'''
Created on 2022/5/1

@author: xckevin1620
'''

from django import template


register=template.Library()

def get_map_val(dictionary,key):
    return dictionary.get(key)

register.filter("get_map_val_by_key", get_map_val)
