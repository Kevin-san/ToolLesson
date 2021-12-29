# -*- coding: UTF-8 -*-
'''
Created on 2019/4/26

@author: xcKev
'''

import datetime
import time
import calendar
import re
import alvintools 

DATE_FORMATS={'yyyy-mm-dd':'%Y-%m-%d','yyyy/mm/dd':'%Y/%m/%d',
              'yyyy-mm-dd HH:mm:ss':'%Y-%m-%d %H:%M:%S', 
              'yyyy/mm/dd HH:mm:ss':'%Y/%m/%d %H:%M:%S',
              'yyyymmdd':'%Y%m%d',
              'mm/dd/yyyy':'%m/%d/%Y',
              'mm/dd/yy':'%m/%d/%y'}
WEEKDAY_MAP={1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat',7:'Sun'}
holiy_file=alvintools.get_holly_file()
print(holiy_file)

class DateConverter(object):

    def __init__(self,holiy_file):
        file_handler=open(holiy_file,'r+')
        self.holiday_list=[]
        file_list=file_handler.readlines()
        for line in file_list:
            mat = re.search(r"\d{4}\d{2}\d{2}",line)
            date_str=mat.group(0)
            if date_str is not None:
                self.holiday_list.append(date_str)

    def date2time(self,date_obj):
        return time.mktime(date_obj.timetuple())

    def time2date(self,time_obj):
        time_res=time.localtime(time_obj)
        date_str=time.strftime('%Y-%m-%d %H:%M:%S',time_res)
        return self.str2date(date_str, '%Y-%m-%d %H:%M:%S')
    
    def str2date(self,date_str,date_format):
        if date_format in DATE_FORMATS.keys():
            return datetime.datetime.strptime(date_str,DATE_FORMATS[date_format])
        return datetime.datetime.strptime(date_str,date_format)

    def date2str(self,date_obj,date_format):
        if date_format in DATE_FORMATS.keys():
            return date_obj.strftime(DATE_FORMATS[date_format])
        return date_obj.strftime(date_format)
    
    def get_datetime(self,year,month,day):
        return datetime.datetime(year,month,day)
    
    def get_week(self,date_obj,date_type='int'):
        week_int=date_obj.isoweekday()
        if date_type == 'str':
            return WEEKDAY_MAP[week_int]
        return week_int
    
    def is_leap(self,year_str):
        return calendar.isleap(int(year_str))
    
    def now(self,date_format=None):
        time_now=datetime.datetime.now()
        if date_format is None:
            return time_now
        return time_now.strftime(date_format)
    
    def today(self):
        return datetime.datetime.today()
    
    def calculate_dates(self,before_of_day,date_format):
        today = self.today()
        calc_dates=[]
        for i in range(0,before_of_day):
            real_i = 0-i-1
            calc_dates.append(self.date2str(self.calc_date(today, real_i), date_format))
        return calc_dates
    
    def is_week_end(self,date_obj):
        week_int = self.get_week(date_obj)
        if week_int==6 or week_int==7:
            return True
        return False
    
    def is_holiday(self,date_obj):
        date_str=self.date2str(date_obj, 'yyyymmdd')
        if date_str in self.holiday_list:
            return True
        return False
    
    def date2timeascstr(self,date_obj):
        return time.asctime(date_obj.timetuple())
    
    #format as yyyymm
    def get_calendar(self,date_str):
        if len(date_str)==4:
            return calendar.calendar(int(date_str))
        if len(date_str)==6:
            return calendar.month(int(date_str[0:4]),int(date_str[4:]))
        return None
        
    def get_weeks(self,date_obj):
        return date_obj.strftime('%W')
    
    def get_month_info(self,date_str):
        if len(date_str)==6:
            return calendar.monthrange(int(date_str[0:4]), int(date_str[4:]))
        return None

    def calc_date(self,date_obj,day_int):
        return date_obj+datetime.timedelta(day_int)
    
    def is_work_day(self,date_obj):
        if self.is_holiday(date_obj) or self.is_week_end(date_obj):
            return False
        return True

    def rol_biz_day(self,date_obj,calc_day_cnt):
        total_cnt = abs(int(calc_day_cnt))
        calc_day = -1 if int(calc_day_cnt) < 0 else 1
        while(total_cnt > 0):
            date_obj=self.calc_date(date_obj,calc_day)
            if self.is_work_day(date_obj):
                total_cnt=total_cnt-1
        return date_obj

    def get_month_biz_end(self,date_str):
        pass
    
    def get_month_biz_beg(self,date_str):
        pass