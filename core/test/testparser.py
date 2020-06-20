# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
from parser import excelreader,filereader,pdfreader
import os

def test_csv_reader():
    csv_file1="C:/Users/xcKev/git/CorePdfPage/practices/filedetails.csv"
    csv_file2="C:/Users/xcKev/git/CorePdfPage/practices/humans.csv"
    fieldnames1=['filename','filesize','filesuffix','filerowcount']
    fieldline1=['test.csv','100bytes','csv',1]
    fieldnames2=['name','age','sex','score','class']
    fieldlines2=[['Xiaoming','22','Man','34','2-1'],['Xiaohong','72','Woman','7','1-1']]
    csvreader1=filereader.CsvReader(csv_file1)
    