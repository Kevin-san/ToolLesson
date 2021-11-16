# -*- coding: utf-8 -*-
'''
Created on 2021/11/11

@author: xcKev
'''
import mistune
import re
from tools import common_tools
from writecreater import pdfwriter

class MarkDownReader(object):
    def __init__(self,markdown_text):
        self.markdown_text=markdown_text
        self.markdown_parser=mistune.BlockLexer(mistune.BlockGrammar())
        self.markdown_outputs=self.markdown_parser.parse(self.markdown_text)
        self.markdown_tokens=[]
    
    def get_markdown_correct_text(self,markdown_text):
        match_links=re.findall(r'\[(.*?)\]\((http.+)\)',markdown_text,flags=0)
        match_images=re.findall(r'!\[\]\((.+)\)',markdown_text,flags=0)
        if match_images:
            markdown_texts=[]
            for match_image in match_images:
                md_image="![]("+match_image+")"
                front_text=markdown_text.split(md_image)[0]
                if front_text != '':
                    markdown_texts.append({'markdown_key':'Paragraph','markdown_val':front_text})
                markdown_texts.append({'markdown_key':'Image','markdown_val':match_image})
                markdown_text=markdown_text.replace(front_text+md_image,'')
            return markdown_texts
        if match_links:
            markdown_texts=[]
            for match_link in match_links:
                match_link_key = match_link[0]
                match_link_val = match_link[1]
                match_link_k= "["+match_link_key+"]"+"("+match_link_val+")"
                front_text=markdown_text.split(match_link_k)[0]
                if front_text != '':
                    markdown_texts.append({'markdown_key':'Paragraph','markdown_val':front_text})
                link_val = match_link_key+":"+match_link_val
                if match_link_val in match_link_key:
                    link_val = match_link_key
                if common_tools.is_dict(markdown_texts[-1]):
                    markdown_texts.append({'markdown_key':'Link','markdown_val':link_val})
                else:
                    markdown_texts.append(link_val)
                markdown_text=markdown_text.replace(front_text,'')
            return markdown_texts
        return markdown_text
    
    def process_markdown_token(self,markdown_output):
        markdown_type = markdown_output['type']
        markdown_text = ''
        if 'text' in markdown_output.keys():
            markdown_text = self.get_markdown_correct_text(markdown_output['text'])
        token=dict()
        if markdown_type == 'heading':
            markdown_key=markdown_type+str(markdown_output['level'])
            token['markdown_key']=markdown_key.capitalize()
            token['markdown_val']=markdown_text
            self.markdown_tokens.append(token)
        elif markdown_type == 'hrule':
            token['markdown_key']='hr'
            token['markdown_val']=''
            self.markdown_tokens.append(token)
        elif markdown_type == 'paragraph':
            if common_tools.is_list(markdown_text):
                for single_token in markdown_text:
                    self.markdown_tokens.append(single_token)
            else:
                token['markdown_key']='Paragraph'
                token['markdown_val']=markdown_text
                self.markdown_tokens.append(token)
        elif markdown_type == 'table':
            markdown_val=[markdown_output['header']]
            for cell in markdown_output['cells']:
                cells = []
                for cel in cell:
                    cel="\n".join(common_tools.get_correct_vals_by_cols_num(12, cel))
                    cells.append(cel)
                markdown_val.append(cells)
            token['markdown_key']='Table'
            token['markdown_val']=markdown_val
            self.markdown_tokens.append(token)
        elif markdown_type =='code':
            token['markdown_key']='Code'
            token['markdown_val']=markdown_text
            self.markdown_tokens.append(token)
        
    def read_markdown(self):
        oul_token=dict()
        for markdown_output in self.markdown_outputs:
            markdown_type = markdown_output['type']
            if markdown_type in ('heading','hrule','paragraph','table','code'):
                self.process_markdown_token(markdown_output)
                
            elif markdown_type=='list_start':
                oul_token['markdown_key']='UnorderedList'
                if markdown_output['ordered']:
                    oul_token['markdown_key']='OrderedList'
                oul_token['markdown_val']=[]
            elif markdown_type in ('list_item_start','list_item_end'):
                continue
            elif markdown_type == 'text' and 'markdown_key' in oul_token.keys():
                oul_token['markdown_val'].append(self.get_markdown_correct_text(markdown_output['text']))
            elif markdown_type == 'list_end':
                self.markdown_tokens.append(oul_token)
                oul_token=dict()
        return self.markdown_tokens


if __name__=='__main__':
    markdown_reader=MarkDownReader('''
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
    pdfwriter.markdown_to_pdf(markdown_outputs,"I:/图片/","/media/img/","E:/lib/books/test.pdf")