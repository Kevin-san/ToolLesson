#-*-coding:utf-8-*-
'''
Created on 2021/9/26

@author: xcKev
'''
from tools import common_coder


NO_ACCESS='你还没有权限访问任何画面！请登录'
EXIST_USER='用户已经存在，请重新选择用户名！'
EXIST_EMAIL='该邮箱地址已被注册，请使用别的邮箱！'
CHECK_VALUE='请检查填写的内容！'
NO_USER='用户不存在！'
NO_CONFIRM='该用户还未通过邮件确认！'
WRONG_PWD='密码不正确！'
DIFF_PWD='两次输入的密码不同！'
INVALID_MSG='无效的确认请求!'
OLD_EMAIL='您的邮件已经过期！请重新注册!'
CONFIRM_LOGIN='感谢确认，请使用账户登录！'

ADD_ACTION='add'
UPD_ACTION='upd'
DETAIL_ACTION='detail'
DETAIL_LIST_ACTION='detaillist'

IS_LOGIN_KEY='is_login'

ERROR_HTML='404.html'
INDEX_HTML='index.html'
CONFIRM_HTML='confirm.html'
LOGIN_HTML='login.html'
REG_HTML='register.html'

USER_PROFILE_HTML='userprofile.html'

FILE_UPLOAD_HTML='fileupload.html'

BLOG_BASE_HTML='blogbase.html'
BLOG_INDEX_HTML='blogindex.html'

BOOK_INDEX_HTML='bookindex.html'
BOOK_BASE_HTML='bookbase.html'

MEDIA_INDEX_HTML='mediaindex.html'
MEDIA_BASE_HTML='mediabase.html'

TOOL_INDEX_HTML='toolindex.html'

# start not in use 
NOVEL_INDEX_HTML='novelindex.html'
NOVEL_BASE_HTML='novelbase.html'

IMAGE_INDEX_HTML='imageindex.html'
IMAGE_BASE_HTML='imagebase.html'

LEARN_INDEX_HTML='learnindex.html'
LEARN_BASE_HTML='learnbase.html'
# end not in use

INDEX_URL='/index'
LOGIN_URL='/login'
USER_PROFILE_URL='/userprofile'

METHOD_POST='POST'

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
