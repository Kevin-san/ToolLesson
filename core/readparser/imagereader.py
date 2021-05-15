# -*- coding: utf-8 -*-
'''
Created on 2020/9/13

@author: xcKev
'''

from cnocr import CnOcr
from tools import common_filer
from writecreater import fileswriter
ocr=CnOcr()
book_dir='E:/lib/books'
pdf_name='regex'
text_path=F'{book_dir}/{pdf_name}.txt'
pdf_path=F'{book_dir}/{pdf_name}'
wrtr = fileswriter.SimpleFileWriter(text_path)
for image_file in common_filer.get_child_files(pdf_path):
    print(image_file)
    res=ocr.ocr(F'{book_dir}/{pdf_name}/{image_file}')
    for each in res:
        if ''.join(each)!='<blank>':
            print(''.join(each))
            wrtr.append_new_line(''.join(each))
wrtr.close()

