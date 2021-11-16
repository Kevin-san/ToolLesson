# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
from PdfWeb.entitys import get_max_length_col_from_table
from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, Paragraph, SimpleDocTemplate, Spacer, Image, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import Drawing, Rect, Circle
from reportlab.lib.colors import HexColor
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.legends import Legend
from pdf2image import convert_from_path
from tools import common_filer, common_tools
import os
from entities.pdfitems import PdfItem
from reportlab.platypus.flowables import ListFlowable

def pdf2images(pdf_path):
    output_file_dir = common_filer.get_file_name(pdf_path)
    parent_dir = common_filer.get_parent_dir(pdf_path)
    output_path=F'{parent_dir}/{output_file_dir}'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    convert_from_path(pdf_path,dpi=100,output_folder=output_path,fmt='jpeg')
    
class SimplePdfWriter(object):
    
    def __init__(self, pdf_file, font_dicts={}, default_fonts={}):
        self.pdf_path = pdf_file
        self.doc = SimpleDocTemplate(self.pdf_path)
        self.font_attrs = default_fonts
        if font_dicts:
            for font_key, font_val in font_dicts.items():
                self.register_font(font_key, font_val)
        style = getSampleStyleSheet()
        self.stylesheet = {}
        self.stylesheet['Title'] = style['Title']
        self.stylesheet['Title'].fontName = 'STSONG'
        self.stylesheet['Normal'] = style['Normal']
        self.stylesheet['Normal'].fontName = 'STSONG'
        self.stylesheet['Heading1'] = style['Heading1']
        self.stylesheet['Heading1'].fontName = 'STSONG'
        self.stylesheet['Heading2'] = style['Heading2']
        self.stylesheet['Heading2'].fontName = 'STSONG'
        self.stylesheet['Heading3'] = style['Heading3']
        self.stylesheet['Heading3'].fontName = 'STSONG'
        self.stylesheet['Heading4'] = style['Heading4']
        self.stylesheet['Heading4'].fontName = 'STSONG'
        self.stylesheet['Heading5'] = style['Heading5']
        self.stylesheet['Heading5'].fontName = 'STSONG'
        self.stylesheet['Heading6'] = style['Heading6']
        self.stylesheet['Heading6'].fontName = 'STSONG'
        self.stylesheet['Code'] = style['Code']
        self.stylesheet['Code'].fontName = 'STSONG'
        self.stylesheet['UnorderedList'] = style['UnorderedList']
        self.stylesheet['UnorderedList'].fontName = 'STSONG'
        self.stylesheet['OrderedList'] = style['OrderedList']
        self.stylesheet['OrderedList'].fontName = 'STSONG'
        self.stylesheet['BodyText'] = style['BodyText']
        self.stylesheet['BodyText'].fontName = 'STSONG'
        self.stylesheet['BodyText'].wordWrap = 'CJK'
        self.stylesheet['BodyText'].firstLineIndent = 32
        self.stylesheet['BodyText'].leading = 30
        self.stylesheet['Table'] = TableStyle(
            [('FONTNAME', (0, 0), (-1, -1), 'STSONG'),
             ('FONTSIZE', (0, 0), (-1, 0), 8),
             ('BACKGROUND', (0, 0), (-1, 0), HexColor('#d5dae6')),
             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
             ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
             ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
             ]
            )
    
    def register_font(self, font_name, font_file):
        pdfmetrics.registerFont(TTFont(font_name, font_file))
    
    def get_table(self, pdf_item):
        dist_list = pdf_item.itemdicts['data']
        col_width = pdf_item.width
        col_height = pdf_item.height
        table_style = pdf_item.itemstyle
        table_obj = Table(dist_list, len(dist_list[0]) * col_width * mm, len(dist_list) * col_height * mm)
        table_obj.setStyle(table_style)
        return table_obj
    
    def get_single_table(self,pdf_item):
        dist_list = pdf_item.itemdicts['data']
        table_style = pdf_item.itemstyle
        table_obj = Table(dist_list)
        table_obj.setStyle(table_style)
        return table_obj
    
    def get_paragraph(self, pdf_item):
        text = pdf_item.itemdicts['text']
        text_style = pdf_item.itemstyle
        return Paragraph(text, text_style)
    
    def get_image(self, pdf_item):
        img = Image(pdf_item.itemdicts['img_path'])
        img.drawWidth = pdf_item.width * mm
        img.drawHeight = pdf_item.height * mm
        return img
    
    def get_spacer(self, pdf_item):
        return Spacer(1, pdf_item.height * mm)
    
    def get_circle(self, pdf_item):
        return Circle(pdf_item.xinch, pdf_item.yinch, pdf_item.width, fillColor=None)
    
    def get_rect(self, pdf_item):
        return Rect(pdf_item.xinch, pdf_item.yinch, pdf_item.width, pdf_item.height, fillColor=None)
    
    def get_bar(self, pdf_item):
        bc = VerticalBarChart()
        bc.x = pdf_item.xinch
        bc.y = pdf_item.yinch
        bc.height = pdf_item.height
        bc.width = pdf_item.width
        bc.data = pdf_item.itemdicts['data']
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = pdf_item.value_max_x
        bc.valueAxis.valueStep = pdf_item.value_step
        bc.categoryAxis.labels.dx = -5
        bc.categoryAxis.labels.dy = -5
        bc.categoryAxis.categoryNames = pdf_item.itemdicts['ax_names']
        return bc
    
    def get_pie(self, pdf_item):
        pie = Pie()
        pie.x = pdf_item.xinch
        pie.y = pdf_item.yinch
        pie.slices.label_boxStrokeColor = colors.white
        
        pie.data = pdf_item.itemdicts['data']
        pie.labels = pdf_item.itemdicts['labels']
        pie.simpleLabels = 0
        pie.sameRadii = 1
        
        pie.slices._strokeColor = colors.blue
        pie.strokeWidth = 1
        pie.strokeColor = colors.white
        pie.slices.label_pointer_piePad = 10
        pie.slices.label_pointer_edgePad = 25
        pie.width = pdf_item.width
        pie.direction = 'clockwise'
        pie.pointerLabelMode = 'LeftRight'
        if 'font_name' in pdf_item.itemdicts.keys():
            for i in range(len(pdf_item.itemdicts['labels'])):
                pie.slices[i].fontName = pdf_item.itemdicts['font_name']
        for i , col in enumerate(pdf_item.itemdicts['colors']):
            pie.slices[i].fillColor = col
        return pie
    
    def get_lineplot(self, pdf_item):
        lp = LinePlot()
        lp.x = pdf_item.xinch
        lp.y = pdf_item.yinch
        lp.height = pdf_item.height
        lp.width = pdf_item.width
        lp.joinedLines = 1
        lp.data = pdf_item.itemdicts['data']
        lp.lineLabelFormat = '%2.0f'
        lp.strokeColor = colors.black
        for i, line_items in enumerate(pdf_item.itemdicts['attrs']):
            lp.lines[i].strokeColor = line_items[0]
            lp.lines[i].symbol = makeMarker(line_items[1])
        lp.xValueAxis.valueMin = 0
        lp.xValueAxis.valueMax = pdf_item.value_max_x
        lp.xValueAxis.valueStep = pdf_item.value_step
        lp.yValueAxis.valueMin = 0
        lp.yValueAxis.valueMax = pdf_item.value_max_y
        lp.yValueAxis.valueStep = pdf_item.value_step
        return lp
        
    
    def get_legend(self, pdf_item):
        leg = Legend()
        leg.fontName = 'Helvetica'
        leg.alignment = 'right'
        leg.boxAnchor = 'ne'
        leg.x = pdf_item.xinch
        leg.y = pdf_item.yinch
        leg.dxTextSpace = 10
        leg.columnMaximum = 2
        leg.colorNamePairs = pdf_item.itemdicts['leg_items']
        return leg
    
    def get_label(self, pdf_item):
        lab = Label()
        lab.x = pdf_item.xinch
        lab.y = pdf_item.yinch
        title = pdf_item.itemdicts['title']
        lab.setText(title)
        if 'font_name' in pdf_item.itemdicts.keys():
            lab.fontName = pdf_item.itemdicts['font_name']
        lab.fontSize = 20
        return lab
    
    def get_drawing_with_complex_charts(self, pdf_items):
        drawing = self.get_drawing(pdf_items[0])
        lab = self.get_label(pdf_items[0])
        item_type = pdf_items[1].itemtype
        if item_type not in ['bar', 'pie', 'lineplot']:
            drawing.add(lab)
            return drawing
        else:
            func = F"get_{item_type}"
            chart = self.func(pdf_items[1])
            leg = self.get_legend(pdf_items[2])
            drawing.add(lab)
            drawing.background = Rect(0, 0, pdf_items[0].width.pdf_items[0].height, strokeWidth=1, strokeColor="#868686", fillColor=None)
            drawing.add(leg)
            drawing.add(chart)
            return drawing
        
    def get_drawing(self, pdf_item):
        return Drawing(pdf_item.width, pdf_item.height)
    
    def write_pages(self, stories):
        page_brk = PageBreak()
        contents = []
        for storys in stories:
            for story in storys:
                contents.append(story)
            contents.append(page_brk)
        self.doc.build(contents)
        return
#     _FilledCircle = _doFill
#     _FilledSquare = _doFill
#     _FilledDiamond = _doFill
#     _FilledCross = _doFill
#     _FilledTriangle = _doFill
#     _FilledStarSix = _doFill
#     _FilledPentagon = _doFill
#     _FilledHexagon = _doFill
#     _FilledHeptagon = _doFill
#     _FilledOctagon = _doFill
#     _FilledStarFive = _doFill
#     _FilledArrowHead = _doFill    
def merge_pdf(in_list, out_file):
    pdf_writer = PdfFileWriter()
    for in_file in in_list:
        pdf_reader = PdfFileReader(open(in_file, 'rb'))
        num_pages = pdf_reader.getNumPages()
        for index in range(0, num_pages):
            page_obj = pdf_reader.getPage(index)
            pdf_writer.addPage(page_obj)
        pdf_writer.write(open(out_file, 'wb'))


def proceed_check_page_cnt(pdf_outputs,pages,cnt,calc_cnt,output_count,items):
    cnt = cnt+calc_cnt
    if cnt< output_count:
        for item in items:
            pdf_outputs.append(item)
    else:
        pages.append(pdf_outputs)
        pdf_outputs=items
        cnt=0+calc_cnt
    return cnt,pages,pdf_outputs

def markdown_to_pdf(markdown_items,image_folder,replace_folder,output_pdf):
    pdf_outputs = []
    pages = []
    cnt = 0
    output_count = 64
    pdf_writer = SimplePdfWriter(output_pdf)
    pdf_writer.register_font('STSONG', "STSONG.TTF")
    for markdown_item in markdown_items:
        markdown_type=markdown_item['markdown_key']
        markdown_val=markdown_item['markdown_val']
        print(markdown_type)
        print(markdown_val)
        if markdown_type == 'Image':
            image_path = markdown_val.replace(replace_folder,image_folder)
            pdf_item=PdfItem.image(image_path,120,80)
            pdf_image=pdf_writer.get_image(pdf_item)
            cnt,pages,pdf_outputs=proceed_check_page_cnt(pdf_outputs,pages,cnt,30,output_count,[pdf_image])
        elif markdown_type in ('Heading1','Heading2','Heading3','Heading4','Heading5','Heading6'):
            pdf_item=PdfItem.paragraph(markdown_val, pdf_writer.stylesheet[markdown_type])
            pdf_paragraph = pdf_writer.get_paragraph(pdf_item)
            cnt,pages,pdf_outputs=proceed_check_page_cnt(pdf_outputs,pages,cnt,1,output_count,[pdf_paragraph])
        elif markdown_type == 'hr':
            pdf_spacer_item = pdf_writer.get_spacer(PdfItem.spacer(1))
            proceed_check_page_cnt(pdf_outputs,pages,cnt,1,output_count,[pdf_spacer_item])
        elif markdown_type == 'Code':
            md_list = markdown_val.split("\n")
            for md_val in md_list:
                pdf_item = PdfItem.paragraph(md_val, pdf_writer.stylesheet[markdown_type])
                pdf_paragraph = pdf_writer.get_paragraph(pdf_item)
                cnt,pages,pdf_outputs=proceed_check_page_cnt(pdf_outputs,pages,cnt,1,output_count,[pdf_paragraph])
        elif markdown_type == 'Table':
            pdf_table=PdfItem.single_table(pdf_writer.stylesheet[markdown_type], markdown_val)
            tab_cnt = len(markdown_val)
            pdf_tab=pdf_writer.get_single_table(pdf_table)
            cnt,pages,pdf_outputs=proceed_check_page_cnt(pdf_outputs,pages,cnt,tab_cnt,output_count,[pdf_tab])
        elif markdown_type == 'UnorderedList':
            ul_list=[]
            for md_val in markdown_val:
                print(md_val)
                item=pdf_writer.get_paragraph(PdfItem.paragraph(md_val, pdf_writer.stylesheet['BodyText']))
                ul_list.append(item)
            tab_cnt = len(ul_list)
            cnt,pages,pdf_outputs=proceed_check_page_cnt(pdf_outputs,pages,cnt,tab_cnt,output_count,[ListFlowable(ul_list,bulletType='bullet',start='square')])
        elif markdown_type == 'OrderedList':
            ol_list=[]
            for md_val in markdown_val:
                item=pdf_writer.get_paragraph(PdfItem.paragraph(md_val, pdf_writer.stylesheet['BodyText']))
                ol_list.append(item)
            tab_cnt = len(ol_list)
            cnt,pages,pdf_outputs=proceed_check_page_cnt(pdf_outputs,pages,cnt,tab_cnt,output_count,[ListFlowable(ol_list,bulletType='i')])
        elif markdown_type== 'Paragraph':
            if markdown_val == "":
                continue
            cnt,pages,pdf_outputs=proceed_check_page_cnt(pdf_outputs,pages,cnt,1,output_count,[pdf_writer.get_paragraph(PdfItem.paragraph(markdown_val, pdf_writer.stylesheet['BodyText']))])
        elif markdown_type == 'Link':
            cnt,pages,pdf_outputs=proceed_check_page_cnt(pdf_outputs,pages,cnt,1,output_count,[pdf_writer.get_paragraph(PdfItem.paragraph(markdown_val, pdf_writer.stylesheet['BodyText']))])
    pages.append(pdf_outputs)
    pdf_writer.write_pages(pages)




if __name__=='__main__':
    pass
#     pdf2images('E:/lib/books/[精通正则表达式(第三版)].（美）佛瑞德.扫描版.pdf')
#     from reportlab.lib.pagesizes import A4
#     print(A4)
#     test_pdf="E:/lib/books/test.pdf"
#     image_path="I:/图片/linux/linux_install7_img_008.png"
#     
#     pdfwriter=SimplePdfWriter(test_pdf)
#     
#     page_item=PdfItem.image(image_path,120,120)
#     page_text=PdfItem.paragraph("Hello World!", text_style=pdfwriter.stylesheet['Normal'])
#     print(type(pdfwriter.get_image(page_item)))
#     stories = [[pdfwriter.get_paragraph(page_text),pdfwriter.get_image(page_item)]]
#     pdfwriter.write_pages(stories)
#    sheet_names=['test1','sheet1','value1']
#    excel_writer=ExcelWriter('C:/Users/xcKev/eclipse-workspace/KToolApps/test/test.xlsx',sheet_names=sheet_names)
#    excel_writer.set_current_sheet('value1')
#    excel_style=ExcelStyle()
#    rows1=['hah','value','mytest']
#    rows2=[1,2,4,5,39,20]
#    columns1=[1230,324432,232432,345]
#    columns2=['hva','cool','clearly']
#    excel_writer.write_row(1, rows1, excel_style.get_style())
#    excel_writer.write_row(2, rows2, excel_style.get_style())
#    excel_writer.write_column(7, columns1, excel_style.get_style())
#    excel_writer.write_column(9, columns2, excel_style.get_style())
#    excel_writer.write_cell_with_formula(2, 8, 'F2+G2')
#    excel_writer.write_hyperlink(3, 8, 'http://www.baidu.com', 'baidu')
#    excel_writer.save()
#     sheet_names=['test1','sheet1','value1']
#     excel_reader=ExcelReader('C:/Users/xcKev/eclipse-workspace/KToolApps/test/test.xls')
#     excel_reader.set_current_sheet('value1')
#     print(excel_reader.get_row_cnt())
#     print(excel_reader.get_col_cnt())
#     print(excel_reader.get_cols(8))
#     print(excel_reader.get_rows(0))
#     print(excel_reader.get_cell(5,7))
#     print(excel_reader.get_hyperlink(5, 7))
#     print(excel_reader.get_formulas())
#     csv_reader=CsvReader('C:/Users/xcKev/eclipse-workspace/KToolApps/test/test.csv',_delimiter='|')
#     print(csv_reader._lines)
#     headers=csv_reader.get_headers(0)
#     print(headers)
#     print(csv_reader._total_cnt)
#     details=csv_reader.get_details(1,4)
#     print(details)

