# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
from alvinreadparser import excelreader,filesreader,pdfreader,markdownreader,\
    htmlreader, textreader
import os
from alvintools.common_tools import get_remote_folder

def test_csv_reader():
    csv_file1="C:/Users/xcKev/git/CorePdfPage/practices/filedetails.csv"
    csv_file2="C:/Users/xcKev/git/CorePdfPage/practices/humans.csv"
    fieldnames1=['filename','filesize','filesuffix','filerowcount']
    fieldline1=['test.csv','100bytes','csv',1]
    fieldnames2=['name','age','sex','score','class']
    fieldlines2=[['Xiaoming','22','Man','34','2-1'],['Xiaohong','72','Woman','7','1-1']]
    csvreader1=filesreader.CsvReader(csv_file1)

def test_markdown_reader():
    markdown_reader=markdownreader.MarkDownReader('''
# Shell 注释
 以 ***  `#` *** 开头的行就是注释，会被解释器忽略。
 通过每一行加一个 ** `#` ** 号设置多行注释，像这样：
 
```bash
#--------------------------------------------
# 这是一个注释
# author：菜鸟教程
# site：www.runoob.com
# slogan：学的不仅是技术，更是梦想！
#--------------------------------------------
##### 用户配置区 开始 #####
#
#
# 这里可以添加脚本描述信息
# 
#
##### 用户配置区 结束  #####
```

如果在开发过程中，遇到大段的代码需要临时注释起来，过一会儿又取消注释，怎么办呢？
每一行加个`#`符号太费力了，可以把这一段要注释的代码用一对花括号括起来，定义成一个函数，没有地方调用这个函数，这块代码就不会执行，达到了和注释一样的效果。

### 多行注释
多行注释还可以使用以下格式：

```bash
:<< EOF
注释内容...
注释内容...
注释内容...
EOF
```

EOF 也可以使用其他符号:

```bash
:<< '
注释内容...
注释内容...
注释内容...
'
:<< !
注释内容...
注释内容...
注释内容...
!
```'''
    )
    markdown_outputs=markdown_reader.read_markdown()
    remote_dir = get_remote_folder()
    markdownreader.pdfwriter.markdown_to_pdf(markdown_outputs,remote_dir+"/图片/","/media/img/","/tmp/test.pdf")

def test_save_mhts_all_images():
    remote_folder = get_remote_folder()
    parent_path = remote_folder+"/图片/Hider/"
    input_path_map={}
    htmlreader.save_mhts_all_images(input_path_map, parent_path)
    
def test_pdf_reader():
    pdf1 = "/tmp/Python修炼之道V1.0.pdf"
    pdf_out = "/tmp/Python修炼之道V1.0_test.txt"
    file_wrtr1 = pdfreader.SimpleFileWriter(pdf_out)
    pdfreader1 = pdfreader.SimplePdfReader(pdf1)
    print(pdfreader1.get_page_structure_dict(6))
    items = pdfreader1.extract_dict_to_items(5)
    for item in items:
        file_wrtr1.append_new_line(item)
    file_wrtr1.close()
    
def test_text_reader():
    sayer = textreader.SimpleTextSayer("在这里，我们在参数中使用了“w”字母，它指示写和加号，这意味着如果库中不存在文件，它将创建一个文件。","/tmp/test.mp3")
    sayer.save_to_file()