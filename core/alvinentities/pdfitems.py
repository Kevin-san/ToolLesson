#-*- encoding:UTF-8 -*-
'''
Created on 2019/12/28

@author: xcKev
'''
import os
def get_val_max(num_list):
    max_val = max(num_list)
    if max_val > 100:
        return 1000
    elif max_val <10 and max_val >0:
        return 10
    return 100

def get_val_step(val_max):
    if val_max == 1000:
        return 100
    elif val_max == 10:
        return 1
    return 10

class PdfLine():
    
    def __init__(self,page,index,span_items,span_count):
        self.page=page
        self.index=index
        self.span_items=span_items
        self.span_count=span_count

class PdfSpan():
    
    def __init__(self,pageno,bbox,pbbox,size,text):
        self.pageno=pageno
        self.x0=bbox[0]
        self.y0=bbox[1]
        self.index=self.y0
        self.x1=bbox[2]
        self.bbox=bbox
        self.pbbox = pbbox
        self.size=size
        self.text=text
        self.item_type="span"
    
    def __str__(self):
        return F"pageno:{self.pageno},x0:{self.x0},y0:{self.y0},x1:{self.x1},size:{self.size},text:{self.text},position:{self.bbox},parent_position:{self.pbbox}"
    
    
class PdfText():
    
    def __init__(self,pageno,bbox,size,text):
        self.pageno=pageno
        self.index=bbox[1]
        self.bbox=bbox
        self.size=size
        self.text=text
        self.item_type="paragraph"
        
    def __str__(self):
        return F"pageno:{self.pageno},index:{self.index},size:{self.size},text:{self.text},position:{self.bbox}"
    

class PdfTable():
    
    def __init__(self,pageno,bbox,size,headers,details):
        self.pageno=pageno
        self.index=bbox[1]
        self.bbox=bbox
        self.size=size
        self.headers=headers
        self.details=details
        self.item_type="table"
    
    def __str__(self):
        return F"pageno:{self.pageno},index:{self.index},size:{self.size},headers:{self.headers},details:{self.details},position:{self.bbox}"
    
class PdfLink():
    
    def __init__(self,pageno,xref,bbox,size,text,to_pageno):
        self.pageno=pageno
        self.index=bbox[1]
        self.bbox=bbox
        self.xref=xref
        self.size=size
        self.text=text
        self.to_pageno=to_pageno
        self.item_type="link"
    
    def __str__(self):
        return F"pageno:{self.pageno},index:{self.index},xref:{self.xref},size:{self.size},to_page:{self.to_pageno},text:{self.text},positions:{self.bbox}"

class PdfImg():
    def __init__(self,pageno,bbox,pdf_image=None):
        self.pageno=pageno
        self.index=bbox[1]
        self.bbox=bbox
        if pdf_image:
            self.xref=pdf_image.xref
            self.ext=pdf_image.ext
            self.imgdata=pdf_image.imgdata
            self.pixn=pdf_image.pixn
        self.item_type="image"
    
    def __str__(self):
        return F"pageno:{self.pageno},index:{self.index},xref:{self.xref},ext:{self.ext},pixn:{self.pixn},imgdata:{self.imgdata},positions:{self.bbox}"
    
    
class PdfImage():
    
    def __init__(self,pageno,xref,ext,imgdata,pixn):
        self.pageno=pageno
        self.xref=xref
        self.ext=ext
        self.imgdata=imgdata
        self.pixn=pixn
    
    def __str__(self):
        return F"pageno:{self.pageno},xref:{self.xref},ext:{self.ext},pixn:{self.pixn},imgdata:{self.imgdata}"
    
class PdfInitParams():
    
    def __init__(self,pdf_file,password=b'',out_file=None,encoding='utf-8',imgdir=None):
        self.pdffile=pdf_file
        self.outfile=out_file
        self.encoding=encoding
        self.password=password
        parentdir=os.path.dirname(pdf_file)
        pdfnamelist=os.path.basename(pdf_file).split('.')
        pdfname='.'.join(pdfnamelist[:-1])
        if self.outfile is None:
            self.outfile=F"{parentdir}/{pdfname}.txt"
        outnamelist=os.path.basename(self.outfile).split('.')
        self.outtype=outnamelist[-1]
        if self.outtype not in ['txt','html','xml','tag']:
            self.outtype='txt'
        self.imgdir=imgdir
        if self.imgdir is None:
            self.imgdir=F"{parentdir}/{pdfname}_images"
        if not os.path.exists(self.imgdir):
            os.makedirs(self.imgdir)
class Position():
    def __init__(self,x=0,y=0,width=0,height=0):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        
class Chart():
    def __init__(self,val_max_x=100,val_max_y=80,val_step=10):
        self.val_max_x=val_max_x
        self.val_max_y=val_max_y
        self.val_step=val_step
    
class PdfItem():
    def __init__(self,position=None,chart=None,item_dicts={},item_type='',style=None):
        if position:
            self.xinch=position.x
            self.yinch=position.y
            self.width=position.width
            self.height=position.height
        if chart:
            self.val_max_x=chart.val_max_x
            self.val_max_y=chart.val_max_y
            self.val_step=chart.val_step
        self.itemdicts=item_dicts
        self.itemstyle=style
        self.itemtype=item_type
    
    @classmethod
    def table(cls,width,height,table_style,dist_list):
        item_dicts={'data':dist_list}
        position=Position(width=width,height=height)
        return cls(position=position,item_type='table',item_dicts=item_dicts,style=table_style)
    
    @classmethod
    def single_table(cls,table_style,dist_list):
        item_dicts={'data':dist_list}
        return cls(item_type='table',item_dicts=item_dicts,style=table_style)
    
    @classmethod
    def paragraph(cls,text_str,text_style):
        item_dicts={'text':text_str}
        return cls(item_dicts=item_dicts,item_type='paragraph',style=text_style)
    
    @classmethod
    def image(cls,img_path,width,height):
        item_dicts={'img_path':img_path}
        position=Position(width=width,height=height)
        return cls(position=position,item_type='image',item_dicts=item_dicts)
    
    @classmethod
    def spacer(cls,height):
        position=Position(height=height)
        return cls(position=position,item_type='spacer')
    
    @classmethod
    def circle(cls,x,y,width):
        position=Position(x=x,y=y,width=width)
        return cls(position=position,item_type='circle')
    
    @classmethod
    def rect(cls,x,y,width,height):
        position=Position(x=x,y=y,height=height,width=width)
        return cls(position=position,item_type='rect')
    
    @classmethod
    def bar(cls,x,y,width,height,data_list,ax_names):
        item_dicts={'data':data_list,'ax_names':ax_names}
        position=Position(x=x,y=y,height=height,width=width)
        x_list=[]
        for tuple_item in data_list:
            for num in tuple_item:
                x_list.append(num)
        val_max_x=get_val_max(x_list)
        val_step=get_val_step(val_max_x)
        chart=Chart(val_max_x=val_max_x,val_step=val_step)
        return cls(position=position,chart=chart,item_dicts=item_dicts,item_type='bar')

    @classmethod
    def pie(cls,x,y,width,data_list,labels,colors):
        item_dicts={'data':data_list,'labels':labels,'colors':colors}
        position=Position(x=x,y=y,width=width)
        return cls(position=position,item_dicts=item_dicts,item_type='pie')
    
    @classmethod
    def lineplot(cls,x,y,width,height,data_list,attrs):
        item_dicts={'data':data_list,'attrs':attrs}
        position=Position(x=x,y=y,height=height,width=width)
        x_list=[]
        y_list=[]
        for item_list in data_list:
            for item_tuple in item_list:
                x_list.append(item_tuple[0])
                y_list.append(item_tuple[1])
        val_max_x=get_val_max(x_list)
        val_max_y=get_val_max(y_list)
        chart=Chart(val_max_x=val_max_x,val_max_y=val_max_y)
        return cls(position=position,item_dicts=item_dicts,item_type='lineplot')
