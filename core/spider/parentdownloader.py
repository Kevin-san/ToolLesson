# -*-coding:utf-8-*-
'''
Created on 2021/7/24

@author: xcKev
'''
from spider.common_spider import current_log
from tools import common_filer
from spider import common_spider
import pymysql
db = pymysql.connect("localhost","root","xc19901109","alvin")
cursor = db.cursor()
class ParentDownloader():
    def __init__(self,folder):
        self.folder = folder
    
    def get_image_spider_source(self):
        sql = "select Name,Id,Section,Url from spidersource where DeleteFlag=1 and Name='图片' order by Id desc"
        cursor.execute(sql)
        source_results = cursor.fetchall()
        for row in source_results:
            name = row[0]
            source_id = str(row[1])
            section = row[2]
            url = row[3]
            directory = self.folder+'/'+name+"/"+section
            common_filer.make_dirs(directory)
            self.get_image_spider_items(directory,source_id,url)
    
    def get_image_spider_items(self,directory,source_id,url):
        sql = 'select distinct si.Name,si.Id from spideritem si,spiderproperty sp where sp.ItemId = si.Id and sp.DeleteFlag = 0 and si.DeleteFlag = 2 and si.SourceId =  %s ' %(source_id)
        current_log.info(sql)
        cursor.execute(sql)
        item_results = cursor.fetchall()
        for row in item_results:
            current_log.info(row)
            name = row[0]
            item_id = row[1]
            img_directory = directory +'/'+name
            common_filer.make_dirs(img_directory)
            self.get_image_spider_properties(name, item_id,img_directory,url)
            
    def get_image_spider_properties(self,name,item_id,directory,url):
        sql = "select OrderId,PropertyBigVal,Id from spiderproperty where DeleteFlag = 0 and ItemId = %s" %(item_id)
        cursor.execute(sql)
        property_results = cursor.fetchall()
        for property_row in property_results:
            current_log.info(property_row)
            order_id = property_row[0]
            img_url = property_row[1]
            property_id = property_row[2]
            self.download_image(name, img_url, order_id,property_id,directory,url)
            
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
        sql = "update spiderproperty set DeleteFlag = 2 where DeleteFlag = 0 and Id = %s" %(property_id)
        current_log.info(sql)
        cursor.execute(sql)
        db.commit()

if __name__=="__main__":
    parent_downloader=ParentDownloader("I:")
    parent_downloader.get_image_spider_source()