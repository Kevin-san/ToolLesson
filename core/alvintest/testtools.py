# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
import alvintools
from alvintools import common_filer,common_spliter ,common_executer,common_dater,common_converter,\
    common_db
from alvinconst import constants
remote_dir = alvintools.get_remote_folder()

def test_common_filer_merge_ts_and_to_mp4():
    common_filer.merge_ts_and_to_mp4(remote_dir+"/Spider/Hider/Video/亚洲无码")

def test_recur_split_novels_in_novel_parent_dir():
    common_spliter.recur_split_novels_in_novel_parent_dir(remote_dir+"/小说/玄幻")

def test_run_python():
    python_log=common_executer.run_python(['print("Hello World!")'])
    print(python_log)

def test_run_golang():
    golang_cmd=['package main','import "fmt"','func main() {','    fmt.Println("Hello, World!")','}']
    golang_log=common_executer.run_go(golang_cmd)
    print(golang_log)
    
def test_run_perl():
    perl_log=common_executer.run_perl(['print "Hello World!";'])
    print(perl_log)
    
def test_run_node():
    node_log=common_executer.run_node_js(["console.log('Hello World!');"])
    print(node_log)

def test_run_java():
    java_cmd='''
public class HelloWorld {
    public static void main(String[] args) {
       System.out.println("Hello World");
    }
}
'''
    java_log=common_executer.run_java([java_cmd])
    print(java_log)

def test_common_dater():
    dateutil=common_dater.DateConverter(holiy_file=common_dater.holiy_file)
    print(dateutil.str2date('2018-12-13', 'yyyy-mm-dd'))
    print(dateutil.str2date('2018/12/13', 'yyyy/mm/dd'))
    print(dateutil.str2date('2018-12-13 23:27:32', 'yyyy-mm-dd HH:mm:ss'))
    print(dateutil.str2date('2018/12/13 23:27:32', 'yyyy/mm/dd HH:mm:ss'))
    print(dateutil.str2date('20181213', 'yyyymmdd'))
    print(dateutil.str2date('12/13/2018', 'mm/dd/yyyy'))
    print(dateutil.str2date('12/13/18', 'mm/dd/yy'))
    date_obj=dateutil.str2date('12/20/19', 'mm/dd/yy')
    print(dateutil.date2str(date_obj, 'yyyymmdd'))
    print(dateutil.date2time(date_obj))
    time_obj=dateutil.date2time(date_obj)
    print(dateutil.time2date(time_obj))
    print(dateutil.is_leap(2000))
    print(dateutil.get_week(date_obj,'str'))
    print(dateutil.is_week_end(date_obj))
    print(dateutil.date2timeascstr(date_obj))
    print(dateutil.get_calendar('2018'))
    print(dateutil.get_calendar('201812'))
    print(dateutil.get_weeks(date_obj))
    print(dateutil.get_month_info('201812'))
    print(dateutil.is_holiday(date_obj))
    print(dateutil.rol_biz_day(date_obj, 3))


def test_common_coverter():
    json_str='''
{
  "rule":{
    "namespace":"strategy",
    "name":"test_exp_1496234234223400",
    "version":0,
    "last_modify_time":1434234236819000,
    "log_rate":1023300,
    "schema_version":"hello_world!"
  },
  "key":"value"
}
'''
    dict_result=common_converter.json2prop(json_str)
    print(dict_result)
    insert_sql_str='''insert into CommonSubFuncs values(470,'sql去除单引号','sql_rem_squote','',27,0,'alvin',curdate());
'''
    print(common_converter.sql_rem_squote(common_converter.sql_add_squote(insert_sql_str)))


def test_common_db(db_handler):
    common_db.execute_ins_upd_del_sql(constants.BOOK_UPD_SQL_AUTHOR, db_handler)
    common_db.execute_ins_upd_del_sql(constants.BOOK_UPD_SQL_INTRO, db_handler)
    common_db.execute_ins_upd_del_sql(constants.BOOK_UPD_SQL_IMAGE, db_handler)
    common_db.execute_ins_upd_del_sql(constants.BOOK_UPD_SQL_LATEST, db_handler)
    common_db.execute_ins_upd_del_sql(constants.SECTION_INS_SQL, db_handler)
    common_db.execute_ins_upd_del_sql(constants.SPIDER_PROPERTY_UPD_FLG_SQL, db_handler)
    common_db.execute_ins_upd_del_sql(constants.MEDIA_UPD_SQL, db_handler)
    common_db.execute_ins_upd_del_sql(constants.SPIDER_ITEM_UPD_SQL, db_handler)
    common_db.execute_ins_upd_del_sql(constants.MEDIA_SECTION_UPD_SQL, db_handler)
    common_db.execute_ins_upd_del_sql(constants.SPIDER_PROPERTY_UPD_FLG_SQL2, db_handler)