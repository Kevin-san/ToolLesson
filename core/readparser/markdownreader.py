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
# Linux 简介


---


Linux 内核最初只是由芬兰人林纳斯·托瓦兹（Linus Torvalds）在赫尔辛基大学上学时出于个人爱好而编写的。
Linux 是一套免费使用和自由传播的类 Unix 操作系统，是一个基于 POSIX 和 UNIX 的多用户、多任务、支持多线程和多 CPU 的操作系统。
Linux 能运行主要的 UNIX 工具软件、应用程序和网络协议。它支持 32 位和 64 位硬件。Linux 继承了 Unix 以网络为核心的设计思想，是一个性能稳定的多用户网络操作系统。

---

## Linux 的发行版

Linux 的发行版说简单点就是将 Linux 内核与应用软件做一个打包。

![](/media/img/linux/linux_intro.jpg)

目前市面上较知名的发行版有：Ubuntu、RedHat、CentOS、Debian、Fedora、SuSE、OpenSUSE、Arch Linux、SolusOS 等。

![](/media/img/linux/linux_systems.jpg)

---
## Linux 应用领域

今天各种场合都有使用各种 Linux 发行版，从嵌入式设备到超级计算机，并且在服务器领域确定了地位，通常服务器使用 LAMP（Linux + Apache + MySQL + PHP）或 LNMP（Linux + Nginx+ MySQL + PHP）组合。
目前 Linux 不仅在家庭与企业中使用，并且在政府中也很受欢迎。
巴西联邦政府由于支持 Linux 而世界闻名。

- 有新闻报道俄罗斯军队自己制造的 Linux 发布版的，做为 G.H.ost 项目已经取得成果。
- 印度的 Kerala 联邦计划在向全联邦的高中推广使用 Linux。
- 中华人民共和国为取得技术独立，在龙芯处理器中排他性地使用 Linux。
-  在西班牙的一些地区开发了自己的 Linux 发布版，并且在政府与教育领域广泛使用，如 Extremadura 地区的 gnuLinEx 和 Andalusia 地区的 Guadalinex。
- 葡萄牙同样使用自己的 Linux 发布版 Caixa Mágica，用于 Magalh?es 笔记本电脑和 e-escola 政府软件。
- 法国和德国同样开始逐步采用 Linux。

---

## Linux vs Windows

目前国内 Linux 更多的是应用于服务器上，而桌面操作系统更多使用的是 Windows。主要区别如下

|比较|Windows|Linux|
| -------- | ----- | ---- |
|界面|界面统一，外壳程序固定所有 Windows 程序菜单几乎一致，快捷键也几乎相同|图形界面风格依发布版不同而不同，可能互不兼容。GNU/Linux 的终端机是从 UNIX 传承下来，基本命令和操作方法也几乎一致。|
|驱动程序|驱动程序丰富，版本更新频繁。默认安装程序里面一般包含有该版本发布时流行的硬件驱动程序，之后所出的新硬件驱动依赖于硬件厂商提供。对于一些老硬件，如果没有了原配的驱动有时很难支持。另外，有时硬件厂商未提供所需版本的 Windows 下的驱动，也会比较头痛。|由志愿者开发，由 Linux 核心开发小组发布，很多硬件厂商基于版权考虑并未提供驱动程序，尽管多数无需手动安装，但是涉及安装则相对复杂，使得新用户面对驱动程序问题（是否存在和安装方法）会一筹莫展。但是在开源开发模式下，许多老硬件尽管在Windows下很难支持的也容易找到驱动。HP、Intel、AMD 等硬件厂商逐步不同程度支持开源驱动，问题正在得到缓解。|
|使用|使用比较简单，容易入门。图形化界面对没有计算机背景知识的用户使用十分有利。|图形界面使用简单，容易入门。文字界面，需要学习才能掌握。|
|学习|系统构造复杂、变化频繁，且知识、技能淘汰快，深入学习困难。|系统构造简单、稳定，且知识、技能传承性好，深入学习相对容易。|
|软件|每一种特定功能可能都需要商业软件的支持，需要购买相应的授权。|大部分软件都可以自由获取，同样功能的软件选择较少。|

---

## Linux的开源共享精神

开源软件最重要的特性如下：

|特性|内容|
| -------- | ----- |
|低风险|使用闭源软件无疑把命运交付给他人，一旦封闭的源代码没有人来维护，你将进退维谷；而且相较于商业软件公司，开源社区很少存在倒闭的问题。|
|高品质|相较于闭源软件公司，开源项目通常是由开源社区来研发及维护，参与编写、维护、测试的用户量众多，一般的bug还没有等爆发就已经被修补。|
|低成本|开源工作者都是在幕后默默且无偿地付出劳动成果，为美好的世界贡献一份力量，因此使用开源社区推动的软件项目可以节省大量的人力、物力和财力。|
|更透明|没有哪个笨蛋会把木马、后门等放到开放的源代码中，这样无疑是把自己的罪行暴露在阳光下。|

## 常用开源软件协议

- GNU GPL( GNU General Public License, GNU通用许可证)
- BSD (Berkeley Software Distribution, 伯克利软件发布版) 许可协议
- Apache 许可证版本(Apache License Version)许可协议
- MPL (Mozilla Public License, Mozilla公共许可)许可协议
- MIT (Massachusetts Institute of Technology)许可协议

'''
    )
    markdown_outputs=markdown_reader.read_markdown()
    pdfwriter.markdown_to_pdf(markdown_outputs,"I:/图片/","/media/img/","E:/lib/books/test.pdf")