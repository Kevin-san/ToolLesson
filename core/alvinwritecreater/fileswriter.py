# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
import csv

class CsvWriter(object):
    def __init__(self, filename, _delimiter=',', _quoting=csv.QUOTE_ALL):
        self._filename = filename
        self.set_csv_format(_delimiter, _quoting)
        self._file_writer = open(self._filename, 'a+', newline='')
        
    def get_csv_writer(self):
        return csv.writer(self._file_writer, 'writer_dialect')
    
    def set_csv_format(self, _delimiter, _quoting):
        csv.register_dialect('writer_dialect', delimiter=_delimiter, quoting=_quoting)
        
    def write_header(self, fieldnames):
        writer = csv.DictWriter(self._file_writer, dialect='writer_dialect', fieldnames=fieldnames)
        writer.writeheader()
    
    def write_line(self, line):
        csv_writer = self.get_csv_writer()
        csv_writer.writerow(line)
    
    def write_lines(self, lines):
        csv_writer = self.get_csv_writer()
        csv_writer.writerows(lines)
class SimpleFileWriter(object):
    def __init__(self,filename,mode='a+'):
        self._filename = filename
        self._file_handler = open(self._filename,mode,encoding='UTF-8')
    
    def append_string(self,string):
        self._file_handler.seek(0,2)
        self._file_handler.write(string)
    
    def append_new_line(self,line):
        self._file_handler.seek(0,0)
        self._file_handler.write(F"\n{line}")
        
    def append_lines(self,lines):
        self._file_handler.writelines(lines)
    
    def close(self):
        self._file_handler.close()