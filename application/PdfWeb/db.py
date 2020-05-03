#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from PdfWeb.models import MenuInfo, LessonMenuIndexInfo,ImageInfo,DetailsInfo


def get_menus(typekey):
    return MenuInfo.objects.filter(MenuType=typekey,DeleteFlag=0)

def get_menu_indexs(typekey):
    return LessonMenuIndexInfo.objects.filter(Type=typekey,DeleteFlag=0)

def get_image(img_name):
    return ImageInfo.objects.filter(ImgKey=img_name,DeleteFlag=0)

def get_details(parent_key):
    return DetailsInfo.objects.filter(ParentKey=parent_key,DeleteFlag=0)

def get_child_details(parent_key):
    return DetailsInfo.objects.filter(ParentKey=parent_key,DeleteFlag=0,ParentFlag=0)

def get_children_detail(parent_key):
    return DetailsInfo.objects.filter(ParentKey__contains=parent_key,DeleteFlag=0,ParentFlag=0)

def get_parent_detail(parent_key):
    key_list=parent_key.split('-')[:-1]
    key_val=key_list[-1]
    typekey='-'.join(key_list[:-1])
    tag_type=key_val.split(':')[0]
    tag_order=key_val.split(':')[1]
    return DetailsInfo.objects.filter(ParentKey=typekey,Type=tag_type,OrderIndex=tag_order,DeleteFlag=0)
