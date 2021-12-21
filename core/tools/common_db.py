#-*- encoding:UTF-8 -*-
'''
Created on 2021/12/18

@author: xcKev
'''

import pymysql
from tools.common_decorator import sql_output
import PdfWeb.constant as constant

def connect_mysql_db(host_port,user,pwd,schema):
    return pymysql.connect(host_port,user,pwd,schema)

def get_localhost_db():
    return connect_mysql_db(constant.MYSQL_HOST_PORT, constant.MYSQL_USER, constant.MYSQL_PWD, constant.MYSQL_SCHEMA)

def get_mysql_cursor(db):
    return db.cursor()

@sql_output
def execute_ins_upd_del_sql(sql_str,db):
    cursor = get_mysql_cursor(db)
    cursor.execute(sql_str)
    db.commit()

@sql_output
def execute_sel_results(sql_str,db):
    cursor = db.cursor()
    cursor.execute(sql_str)
    results = cursor.fetchall()
    return results

@sql_output
def execute_sel_no_result(sql_no_str,db):
    cursor = db.cursor()
    cursor.execute(sql_no_str)
    results = cursor.fetchall()
    return int(results[0][0])
