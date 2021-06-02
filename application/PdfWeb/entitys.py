#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
import tools.common_tools as common
import os
from PdfWeb.models import Article

def get_val_max(num_list):
    max_val = max(num_list)
    if max_val > 100:
        return 1000
    elif max_val <10 and max_val >0:
        return 10
    return 100

def convert_common_rules_to_tag_dict(rule_list):
    tag_dict=dict()
    for common_rule in rule_list:
        tag_dict[common_rule.TypeVal]=common_rule
    return tag_dict

class PdfInitParams():
    
    def __init__(self,pdf_file,password=b'',out_file=None,encoding='utf-8',imgdir=None):
        self.pdffile=pdf_file
        self.outfile=out_file
        self.encoding=encoding
        self.password=password
        parentdir=os.path.dirname(pdf_file)
        pdfnamelist=os.path.basename(pdf_file).split('.')
        pdfname='.'.join(pdfnamelist[:-1])
        if self.outfile is None:
            self.outfile=F"{parentdir}/{pdfname}.txt"
        outnamelist=os.path.basename(self.outfile).split('.')
        self.outtype=outnamelist[-1]
        if self.outtype not in ['txt','html','xml','tag']:
            self.outtype='txt'
        self.imgdir=imgdir
        if self.imgdir is None:
            self.imgdir=F"{parentdir}/{pdfname}_images"
        if not os.path.exists(self.imgdir):
            os.makedirs(self.imgdir)
class Position():
    def __init__(self,x=0,y=0,width=0,height=0):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        
class Chart():
    def __init__(self,val_max_x=100,val_max_y=80,val_step=10):
        self.val_max_x=val_max_x
        self.val_max_y=val_max_y
        self.val_step=val_step
    
class PdfItem():
    def __init__(self,position=None,chart=None,item_dicts={},item_type='',style=None):
        self.xinch=position.x
        self.yinch=position.y
        self.width=position.width
        self.height=position.height
        self.val_max_x=chart.val_max_x
        self.val_max_y=chart.val_max_y
        self.val_step=chart.val_step
        self.itemdicts=item_dicts
        self.itemstyle=style
        self.itemtype=item_type
    
    @classmethod
    def table(cls,width,height,table_style,dist_list):
        item_dicts={'data':dist_list}
        position=Position(width=width,height=height)
        return cls(position=position,item_type='table',item_dicts=item_dicts,style=table_style)
    
    @classmethod
    def paragraph(cls,text_str,text_style):
        item_dicts={'text':text_str}
        return cls(item_dicts=item_dicts,item_type='paragraph',style=text_style)
    
    @classmethod
    def image(cls,img_path,width,height):
        item_dicts={'img_path':img_path}
        position=Position(width=width,height=height)
        return cls(position=position,item_type='image',item_dicts=item_dicts)
    
    @classmethod
    def spacer(cls,height):
        position=Position(height=height)
        return cls(position=position,item_type='spacer')
    
    @classmethod
    def circle(cls,x,y,width):
        position=Position(x=x,y=y,width=width)
        return cls(position=position,item_type='circle')
    
    @classmethod
    def rect(cls,x,y,width,height):
        position=Position(x=x,y=y,height=height,width=width)
        return cls(position=position,item_type='rect')
    
    @classmethod
    def bar(cls,x,y,width,height,data_list,ax_names,val_step):
        item_dicts={'data':data_list,'ax_names':ax_names}
        position=Position(x=x,y=y,height=height,width=width)
        x_list=[]
        for tuple_item in data_list:
            for num in tuple_item:
                x_list.append(num)
        val_max_x=get_val_max(x_list)
        chart=Chart(val_max_x=val_max_x,val_step=val_step)
        return cls(position=position,chart=chart,item_dicts=item_dicts,item_type='bar')

    @classmethod
    def pie(cls,x,y,width,data_list,labels,colors):
        item_dicts={'data':data_list,'labels':labels,'colors':colors}
        position=Position(x=x,y=y,width=width)
        return cls(position=position,item_dicts=item_dicts,item_type='pie')
    
    @classmethod
    def lineplot(cls,x,y,width,height,data_list,attrs):
        item_dicts={'data':data_list,'attrs':attrs}
        position=Position(x=x,y=y,height=height,width=width)
        x_list=[]
        y_list=[]
        for item_list in data_list:
            for item_tuple in item_list:
                x_list.append(item_tuple[0])
                y_list.append(item_tuple[1])
        val_max_x=get_val_max(x_list)
        val_max_y=get_val_max(y_list)
class Property():
    def __init__(self,property_type,property_name):
        self.property_type=property_type
        self.property_name=common.to_camel(property_name)
        self.m_prop_name=common.to_normalize(self._property_name)
        
class Method():
    def __init__(self,method_name,method_type,property_list,method_content=""):
        self.method_name=method_name
        self.method_type=method_type
        self.property_list=property_list
        self.method_content=method_content

class Column(object):
    
    def __init__(self,col_type,col_name):
        self.col_type=col_type
        self.col_name=common.to_underscore(col_name)

class HomeIndexItem():
    def __init__(self,id_name,menu_title,menu_infos):
        self.id = id_name
        self.title = menu_title
        self.infos = menu_infos

class HomeInfoItem():
    def __init__(self,book_lesson,image_content):
        self.LessonHref = book_lesson.LessonHref
        self.LessonName = book_lesson.LessonName
        self.Description = book_lesson.Description
        self.ImageName = image_content.ImageName
        self.Width = image_content.Width
        self.Height = image_content.Height
        

class PageInfoItem():
    def __init__(self,page_no,page_url):
        self.page_no=page_no
        self.page_url=page_url