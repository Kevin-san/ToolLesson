#-*- encoding:UTF-8 -*-
'''
Created on 2021/7/24

@author: xcKev
'''
from alvinspider.common_spider import current_log
from alvintools import common_filer,common_db
from alvinspider import common_spider
import alvinconst.constants as constant

class ParentDownloader():
    def __init__(self,folder,db):
        self.folder = folder
        self.db = db
    
    def get_image_spider_source(self):
        sql = constant.SPIDER_SOURCE_SEL_IMAGE_SQL
        source_results = common_db.execute_sel_results(sql, self.db)
        for row in source_results:
            name = row[0]
            source_id = str(row[1])
            section = row[2]
            url = row[3]
            directory = self.folder+'/'+name+"/"+section
            common_filer.make_dirs(directory)
            self.get_image_spider_items(directory,source_id,url)
    
    def get_image_spider_source_by_grps(self):
        sql = constant.SPIDER_SOURCE_SEL_IMAGE_SQL
        source_results = common_db.execute_sel_results(sql, self.db)
        source_cnt = len(source_results)
        while True:
            total_empty_cnt = 0
            for row in source_results:
                name = row[0]
                source_id = str(row[1])
                section = row[2]
                url = row[3]
                directory = self.folder+'/'+name+"/"+section
                common_filer.make_dirs(directory)
                exec_cnt=self.get_first_image_spider_item(directory,source_id,url)
                if exec_cnt == 0:
                    total_empty_cnt = total_empty_cnt+1
            if total_empty_cnt == source_cnt:
                break
    
    def get_first_image_spider_item(self,directory,source_id,url):
        sql = constant.SPIDER_ITEM_SEL_SINGLE_ITEM_BY_SOURCE_SQL_TEMPLATE %(source_id)
        item_results = common_db.execute_sel_results(sql, self.db)
        if len(item_results) == 0:
            return 0
        row=item_results[0]
        current_log.info(row)
        name = row[0]
        item_id = row[1]
        img_directory = directory +'/'+name
        common_filer.make_dirs(img_directory)
        self.get_image_spider_properties(name, item_id,img_directory,url)
        return 1
    
    def get_novel_spider_source(self):
        sql = constant.SPIDER_SOURCE_SEL_NOVEL_SQL
        source_results = common_db.execute_sel_results(sql, self.db)
        for row in source_results:
            name = row[0]
            source_id = str(row[1])
            section = row[2]
            url = row[3]
            directory = self.folder+'/'+name+"/"+section
            common_filer.make_dirs(directory)
            self.get_novel_spider_items(directory,source_id,url)
    
    def get_image_spider_items(self,directory,source_id,url):
        sql = constant.SPIDER_ITEM_SEL_ITEM_BY_SOURCE_SQL_TEMPLATE %(source_id)
        item_results = common_db.execute_sel_results(sql, self.db)
        for row in item_results:
            current_log.info(row)
            name = row[0]
            item_id = row[1]
            img_directory = directory +'/'+name
            common_filer.make_dirs(img_directory)
            self.get_image_spider_properties(name, item_id,img_directory,url)
    
    def get_novel_spider_items(self,directory,source_id):
        sql = constant.SPIDER_ITEM_SEL_ITEM_BY_SOURCE_SQL_TEMPLATE %(source_id)
        item_results = common_db.execute_sel_results(sql, self.db)
        for row in item_results:
            current_log.info(row)
            name = row[0]
            item_id = row[1]
            img_directory = directory +'/'+name
            common_filer.make_dirs(img_directory)
            self.get_novel_spider_properties(item_id,img_directory)
    
    def get_image_spider_properties(self,name,item_id,directory,url):
        sql = constant.SPIDER_PROPERTY_SEL_SQL_TEMPLATE %(item_id)
        property_results = common_db.execute_sel_results(sql, self.db)
        for property_row in property_results:
            current_log.info(property_row)
            order_id = property_row[0]
            img_url = property_row[1]
            property_id = property_row[2]
            self.download_image(name, img_url, order_id,property_id,directory,url)
            
    def get_novel_spider_properties(self,item_id,directory):
        sql = constant.SPIDER_PROPERTY_SEL_SQL_CHAPTER_TEMPLATE %(item_id)
        property_results = common_db.execute_sel_results(sql, self.db)
        for property_row in property_results:
            current_log.info(property_row)
            novel_title = property_row[0]
            novel_val = property_row[1]
            property_id = property_row[2]
            self.download_novel(novel_title, novel_val,property_id,directory)
    
    def download_novel(self,novel_title,novel_val,property_id,directory):
        novel=novel_title+".txt"
        cur_file = directory + '/' + novel
        current_log.info(cur_file)
        if common_filer.exists(cur_file) and common_filer.get_file_size(cur_file) >0:
            current_log.info("The file %s exists" %(cur_file))
            self.update_image_spider_property(property_id)
        else:
            file_w=open(cur_file,'w+')
            file_w.write(novel_val)
            file_w.close()
            current_log.info("The file %s downloaded" %(cur_file))
            self.update_image_spider_property(property_id)
        
        
    def download_image(self,name,img_url,order_id,property_id,directory,url):
        img_name=name+'_'+str(order_id)+'.'+img_url.split('/')[-1].split('.')[-1]
        cur_file = directory + '/' + img_name
        current_log.info(cur_file)
        if common_filer.exists(cur_file):
            current_log.info("The file %s exists" %(cur_file))
            self.update_image_spider_property(property_id)
        else:
            if url == 'https://www.mzitu.com/':
                res= common_spider.get_response_by_seconds(img_url, '','',0,url)
            else:
                res= common_spider.get_response_by_seconds(img_url, '','',0)
            file_w=open(cur_file,'wb')
            file_w.write(res.content)
            file_w.close()
            current_log.info("The file %s downloaded" %(cur_file))
            self.update_image_spider_property(property_id)
            
    def update_image_spider_property(self,property_id):
        sql = constant.SPIDER_PROPERTY_UPD_FLG_TWO_SQL_TEMPLATE %(property_id)
        common_db.execute_ins_upd_del_sql(sql, self.db)