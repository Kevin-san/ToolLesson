#-*- encoding:UTF-8 -*-
'''
Created on 2021/12/28

@author: xcKev
'''
from alvintools import common_coder

MYSQL_HOST_PORT='192.168.31.103'
MYSQL_USER='root'
MYSQL_SCHEMA='alvin'
MYSQL_ENC_KEY='alvin'
MYSQL_ENC_PWD='Ep0IjqfwDUM21w=='
MYSQL_PWD=common_coder.decode2rc4(MYSQL_ENC_PWD, MYSQL_ENC_KEY)


SPIDER_SOURCE_SEL_SQL="select * from SpiderSource where DeleteFlag = 0"
SPIDER_SOURCE_SEL_IMAGE_SQL="select Name,Id,Section,Url from SpiderSource where DeleteFlag=1 and Name='图片' order by Id desc"
SPIDER_SOURCE_SEL_NOVEL_SQL="select Name,Id,Section,Url from SpiderSource where DeleteFlag=1 and Name='小说' order by Id"
SPIDER_SOURCE_UPD_SQL_TEMPLATE="update SpiderSource set DeleteFlag = 1 where Id = %s "
SPIDER_RULE_SEL_SQL="select * from SpiderRule where DeleteFlag = 0 order by Id"
SPIDER_ITEM_INS_SQL_TEMPLATE="insert into SpiderItem(SourceId,Url,Name,submission_date) values(%s,'%s','%s',curdate())"
SPIDER_ITEM_SEL_SQL_TEMPLATE="select * from SpiderItem where DeleteFlag = 0 and instr(Url,'%s') = 1 ORDER BY SourceId DESC limit 1"
SPIDER_ITEM_SEL_SINGLE_ITEM_BY_SOURCE_SQL_TEMPLATE='select distinct si.Name,si.Id from SpiderItem si,SpiderProperty sp where sp.ItemId = si.Id and sp.DeleteFlag = 0 and si.DeleteFlag = 2 and si.SourceId =  %s limit 1'
SPIDER_ITEM_SEL_ITEM_BY_SOURCE_SQL_TEMPLATE='select distinct si.Name,si.Id from SpiderItem si,SpiderProperty sp where sp.ItemId = si.Id and sp.DeleteFlag = 0 and si.DeleteFlag = 2 and si.SourceId =  %s '
SPIDER_ITEM_SEL_URL_SQL='select Url from SpiderItem group by Url having count(Id) > 1'
SPIDER_ITEM_SEL_ID_TEMPLATE="select Id from SpiderItem where Url = '%s'"
SPIDER_ITEM_DEL_SQL_TEMPLATE="delete from SpiderItem where Id = %s"
SPIDER_ITEM_UPD_FLG_TWO_SQL_TEMPLATE="update SpiderItem set DeleteFlag = 2 where Id = %s"
SPIDER_ITEM_UPD_FLG_THREE_SQL_TEMPLATE="update SpiderItem set DeleteFlag = 3 where Id = %s"
SPIDER_ITEM_UPD_FLG_ONE_SQL_TEMPLATE="update SpiderItem set DeleteFlag = 1 where Id = %s"
SPIDER_PROPERTY_DEL_SQL_TEMPLATE="delete from SpiderProperty where ItemId = %s"
SPIDER_PROPERTY_CNT_SQL_TEMPLATE="select count(*) from SpiderProperty where ItemId = %s and OrderId = %s"
SPIDER_PROPERTY_INS_SQL_TEMPLATE="insert SpiderProperty(ItemId,OrderId,PropertyKey,PropertyValue,PropertyBigVal,submission_date) values(%s,%s,'%s','%s','%s',curdate())"
SPIDER_PROPERTY_UPD_SQL_TEMPLATE="update SpiderProperty set PropertyValue = '%s' , PropertyBigVal = '%s' where ItemId = %s and PropertyKey = '%s' and OrderId =%s"
SPIDER_PROPERTY_UPD_FLG_TWO_SQL_TEMPLATE="update SpiderProperty set DeleteFlag = 2 where DeleteFlag = 0 and Id = %s"
SPIDER_PROPERTY_SEL_CNT_SQL_TEMPLATE="select count(*) from SpiderProperty where ItemId = %s and PropertyKey = '%s'"
SPIDER_PROPERTY_SEL_MAX_ORDID_SQL_TEMPLATE="select max(OrderId) from SpiderProperty where ItemId = %s and PropertyKey = '章节'"
SPIDER_PROPERTY_SEL_SQL_TEMPLATE="select OrderId,PropertyBigVal,Id from SpiderProperty where DeleteFlag = 0 and ItemId = %s"
SPIDER_PROPERTY_SEL_SQL_CHAPTER_TEMPLATE="select PropertyVal,PropertyBigVal,Id from SpiderProperty where DeleteFlag = 0 and ItemId = %s and PropertyKey = '章节'"
SPIDER_CATEGORY_SEL_SQL_TEMPLATE='select CategoryId,CategoryName,CategoryValue1 from Category where DeleteFlag=0 and CategoryFather=%s order by CategoryId desc'
SPIDER_TRIGGER_SEL_SQL_TEMPLATE='select Id,Url,RequestUrl,TriggerCategoryId,TriggerParams,TriggerCategoryKey,MapUrl,DownloadFolder from SpiderTrigger where DeleteFlag = 0 and TriggerCategoryId = %s'
SPIDER_TRIGGER_INS_SQL_TEMPLATE="insert into SpiderTriggerResult(TriggerId,CategoryFather,CategoryId,CoverImg,Title,VUrl,DownloadFolder,submission_date) values(%s,%s,%s,'%s','%s','%s','%s',curdate())"
SPIDER_TRIGGER_SEL_SINGLE_ACTIVE_SQL="select Id,Title,VUrl,DownloadFolder from SpiderTriggerResult where DeleteFlag =0 limit 1"
SPIDER_TRIGGER_SEL_INACTIVE_SQL="select Id,Title,VUrl,DownloadFolder from SpiderTriggerResult where DeleteFlag =1 order by Id desc"
SPIDER_TRIGGER_UPD_SQL_TEMPLATE="update SpiderTriggerResult set DeleteFlag = 1 where Id = %s"
SPIDER_TRIGGER_UPD_INACTIVE_SQL_TEMPLATE="update SpiderTriggerResult set DeleteFlag = 2 where Id = %s"

BOOK_UPD_SQL_AUTHOR="update Book b INNER JOIN SpiderProperty sp ON b.Id=sp.ItemId AND sp.PropertyKey='作者' set b.Author = sp.PropertyValue;"
BOOK_UPD_SQL_INTRO="update Book b INNER JOIN SpiderProperty sp ON b.Id=sp.ItemId AND sp.PropertyKey='简介' set b.Description = sp.PropertyValue;"
BOOK_UPD_SQL_IMAGE="update Book b INNER JOIN SpiderProperty sp ON b.Id=sp.ItemId AND sp.PropertyKey='图片' set b.ImageContent = case when sp.PropertyValue = '' then '/img/novel_bg.jpg' else sp.PropertyValue end;"
BOOK_UPD_SQL_LATEST="update Book b INNER JOIN SpiderProperty sp ON b.Id=sp.ItemId AND sp.PropertyKey='最新' set b.MaxSectionId = sp.PropertyValue , b.MaxSectionName = sp.PropertyBigVal;"
SECTION_INS_SQL="insert into Section(BookId,OrderNo,SectionNo,ChapterName,Content,UpdateTime,UpdateUser,DeleteFlag,submission_user,submission_date) SELECT si.Id,sp.OrderId,0,sp.PropertyValue,sp.PropertyBigVal,now(),'alvin',0,'alvin',CURDATE() FROM SpiderProperty sp,SpiderItem si WHERE si.Id = sp.ItemId AND sp.PropertyKey = '章节' AND sp.DeleteFlag = 0 and si.SourceId=8;"
SPIDER_PROPERTY_UPD_FLG_SQL="update SpiderProperty set DeleteFlag  = -2 where DeleteFlag = 0 and PropertyKey = '章节';"
MEDIA_UPD_SQL="insert into Media SELECT Id,Name,CONCAT('/img/美女/',Name,''),'','',CONCAT('/img/美女/',Name,CONCAT('/',Name,'_0.jpg')),SourceId+200,0,0,now(),'alvin',0,'alvin',curdate() FROM SpiderItem WHERE SourceId >=15 AND DeleteFlag = 2;"
SPIDER_ITEM_UPD_SQL="update SpiderItem set DeleteFlag = -2 where SourceId >=15 AND DeleteFlag = 2;"
MEDIA_SECTION_UPD_SQL="insert into MediaSection(MediaId,OrderNo,SectionNo,Preffix,Time,Size,UpdateTime,UpdateUser,DeleteFlag,submission_user,submission_date) SELECT ItemId,OrderId,0,'jpg',0,0,now(),'alvin',0,'alvin',curdate() FROM SpiderProperty WHERE PropertyKey = '序号' and DeleteFlag = 2;"
SPIDER_PROPERTY_UPD_FLG_SQL2="update SpiderProperty set DeleteFlag  = -2 where DeleteFlag = 2 and PropertyKey = '序号';"