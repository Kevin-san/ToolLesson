# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
import csv

def get_csv_columns(in_file, seperator_char, from_row_id, to_row_id, column_id):
    in_file_h = open(in_file, 'rt')
    csv.register_dialect('mydialect', delimiter=seperator_char, quoting=csv.QUOTE_MINIMAL)
    csv_read_h = csv.reader(in_file_h, 'mydialect')
    org_lines = []
    for line in csv_read_h:
        org_lines.append(line)
    result_lines = []
    from_row_id = int(from_row_id)
    to_row_id = int(to_row_id)
    column_id = int(column_id)
    if to_row_id == -1:
        to_row_id = int(len(org_lines))
    for row_id in range(from_row_id, to_row_id):
        result_line = org_lines[row_id]
        result_lines.append(result_line[column_id])
    return result_lines

class SimpleFileReader(object):
    
    def __init__(self,filename):
        self._filehandler=open(filename,'r',encoding='UTF-8')
        
    def read(self,lineno=None):
        if lineno is None:
            return self._filehandler.read()
        return self._filehandler.read(lineno)
    
    def read_line(self,lineno=None):
        if lineno is None:
            return self._filehandler.readline()
        return self._filehandler.readline(lineno)
    
    def read_lines(self):
        return self._filehandler.readlines()
    
    def get_file_position(self):
        return self._filehandler.tell()
    
    def close(self):
        return self._filehandler.close()


class CsvReader(object):
    
    def __init__(self, filename, _delimiter=',', _quoting=csv.QUOTE_ALL):
        self._filename = filename
        self.set_csv_format(_delimiter, _quoting)
        self._file_reader = open(self._filename, 'rt')
        self._lines = self.read_lines()
        self._total_cnt = self.get_total_line_num()
    
    def get_csv_reader(self):
        return csv.reader(self._file_reader, 'reader_dialect')
    
    def set_csv_format(self, _delimiter, _quoting):
        csv.register_dialect('reader_dialect', delimiter=_delimiter, quoting=_quoting)
        
    def read_lines(self):
        lines = []
        reader = self.get_csv_reader()
        for line in reader:
            lines.append(line)
        return lines
    def get_total_line_num(self):
        if self._lines:
            return len(self._lines)
        return 0
    
    def get_headers(self, index=0):
        if self._lines:
            return self._lines[index]
        return []
    
    def get_details(self, begin_index, end_index):
        details = []
        if begin_index < end_index and end_index <= self._total_cnt:
            for i in range(begin_index, end_index):
                details.append(self._lines[i])
        return details
