#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
import alvintools.common_tools as common
import os

def get_val_max(num_list):
    max_val = max(num_list)
    if max_val > 100:
        return 1000
    elif max_val <10 and max_val >0:
        return 10
    return 100

def get_max_length(cols):
    max_length_col = max(cols)
    return len(max_length_col)

def get_max_length_col_from_table(table_list):
    reverse_tables=[[row[i] for row in table_list] for i in range(len(table_list[0]))]
    max_cols_list = []
    for cols in reverse_tables:
        max_cols_list.append(cols)
    return get_max_length(max_cols_list)

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

class PageInfoItem():
    def __init__(self,page_no,page_url):
        self.page_no=page_no
        self.page_url=page_url
        
class SpiderSourceEntity():
    def __init__(self,Id,Name,Section,Url,Attr,DeleteFlag):
        self.Id=Id
        self.Name=Name
        self.Section=Section
        self.Url=Url
        self.Attr=Attr
        self.DeleteFlag=DeleteFlag
    
class SpiderItemEntity():
    def __init__(self,Id,SourceId,Url,Name,DeleteFlag):
        self.Id=Id
        self.SourceId=SourceId
        self.Url=Url
        self.Name=Name
        self.DeleteFlag=DeleteFlag

class SpiderPropertyEntity():
    def __init__(self,Id,ItemId,OrderId,PropertyKey,PropertyValue,PropertyBigVal,DeleteFlag):
        self.Id=Id
        self.ItemId=ItemId
        self.OrderId=OrderId
        self.PropertyKey=PropertyKey
        self.PropertyValue=PropertyValue
        self.PropertyBigVal=PropertyBigVal
        self.DeleteFlag=DeleteFlag

class NovelInfoItem():
    def __init__(self,item_id,novel_name,author,intro,last_upd_content_id,last_upd_content_title):
        self.item_id = item_id
        self.novel_name=novel_name
        self.author=author
        self.intro=intro
        self.last_upd_content_id = last_upd_content_id
        self.last_upd_content_title = last_upd_content_title



class BookIndexItem():
    def __init__(self,book,sections):
        self.book = book
        self.sections = sections

class BookContentItem():
    def __init__(self,parent_item_id,cur_content,prev_content_id=None,next_content_id=None):
        self.parent_item_id = parent_item_id
        self.cur_content= cur_content
        self.prev_content_id=prev_content_id
        self.next_content_id=next_content_id

