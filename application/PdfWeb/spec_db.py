#-*- encoding:UTF-8 -*-
'''
Created on 2021/12/18

@author: xcKev
'''

from PdfWeb.entitys import NovelInfoItem, SpiderSourceEntity, SpiderItemEntity, SpiderPropertyEntity
from tools import common_db
db = common_db.get_localhost_db()


def select_spider_source(select_sql):
    result_list=[]
    for row in common_db.execute_sel_results(select_sql, db):
        spider_source = SpiderSourceEntity(row[0],row[1],row[2],row[3],row[4],row[5])
        result_list.append(spider_source)
    return result_list

def select_spider_item(select_sql):
    result_list=[]
    for row in common_db.execute_sel_results(select_sql, db):
        spider_item = SpiderItemEntity(row[0],row[1],row[2],row[3],row[4])
        result_list.append(spider_item)
    return result_list

def select_spider_props(select_sql):
    result_list=[]
    for row in common_db.execute_sel_results(select_sql, db):
        spider_prop = SpiderPropertyEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        result_list.append(spider_prop)
    return result_list

def select_spider_prop_max_order_map():
    select_sql = "SELECT ItemId,max(OrderId) FROM SpiderProperty WHERE PropertyKey = '章节' group by ItemId"
    result_map=dict()
    for row in common_db.execute_sel_results(select_sql, db):
        result_map[row[0]]=row[1]
    return result_map

def select_novel_infos(select_sql):
    result_list=[]
    for row in common_db.execute_sel_results(select_sql, db):
        novel_info = NovelInfoItem(row[0], row[1], row[2], row[3],row[4],row[5])
        result_list.append(novel_info)
    return result_list

def get_spider_source(source_name):
    select_sql="select * from SpiderSource where Name= '%s' and DeleteFlag = %s order by Id" %(source_name,1)
    return select_spider_source(select_sql)

def get_spider_item_by_id(item_id):
    select_sql="select * from SpiderItem where Id= %s order by Id" %(item_id)
    return select_spider_item(select_sql)[0]

def get_spider_item_property(source_id):
    select_sql="select * from SpiderItem where SourceId= %s and DeleteFlag !=0 order by Id" %(source_id)
    return select_spider_item(select_sql)

def get_spider_item_by_page_no(source_id,page_no,count):
    if page_no == 1:
        begin_no = 0
    else:
        begin_no = (int(page_no)-1) * count
    select_sql="select * from SpiderItem where SourceId= %s and DeleteFlag !=0 order by Id limit %s,%s" %(source_id,begin_no,count)
    return select_spider_item(select_sql)

def get_spider_property(item_id):
    select_sql="select * from SpiderProperty where ItemId= %s order by Id" %(item_id)
    return select_spider_props(select_sql)

def get_spider_property_by_property_id(property_id):
    select_sql="select * from SpiderProperty where Id= %s order by Id" %(property_id)
    return select_spider_props(select_sql)[0]

def get_spider_property_by_order_id(item_id,order_id):
    if order_id is None:
        return None
    select_sql="select * from SpiderProperty where ItemId= %s and OrderId = %s order by Id" %(item_id,order_id)
    return select_spider_props(select_sql)[0]

def get_spider_property_with_prop_key(item_id,prop_key):
    select_sql="select * from SpiderProperty where ItemId= %s and PropertyKey = '%s' order by Id" %(item_id,prop_key)
    return select_spider_props(select_sql)

def get_spider_property_with_max_order_id(item_id,prop_key):
    select_sql="select * from SpiderProperty where ItemId= %s and PropertyKey = '%s' order by OrderId desc" %(item_id,prop_key)
    return select_spider_props(select_sql)

def get_spider_property_by_author_name(author_name):
    select_sql="select si.Id,si.Name,sp1.PropertyValue,sp2.PropertyValue,sp3.PropertyValue,sp3.PropertyBigVal FROM SpiderItem si,SpiderProperty sp1,SpiderProperty sp2,SpiderProperty sp3 where sp1.PropertyValue= '%s' and sp1.PropertyKey = '%s' and sp1.ItemId = si.Id AND si.Id = sp2.ItemId AND sp2.PropertyKey = '简介' AND si.Id = sp3.ItemId AND sp3.PropertyKey = '最新'" %(author_name,'作者')
    return select_novel_infos(select_sql)

def get_image_item_count_by_source_id(source_id):
    select_sql = "SELECT count(*) FROM SpiderItem WHERE SourceId = %s AND DeleteFlag =2 " %(source_id)
    return common_db.execute_sel_no_result(select_sql, db)