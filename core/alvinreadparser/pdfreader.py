# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
import fitz
import time
from alvinwritecreater.fileswriter import SimpleFileWriter
from alvintools import common_filer, common_tools, common_logger
from alvinentities.pdfitems import PdfImage, PdfImg, PdfText, PdfLink, PdfTable, PdfSpan
from aip import AipOcr
APP_ID='22838451'
API_KEY='bmz77GlmsKDlLsHd1zDGsMlx'
SERCRET_KEY = 'B4I96wFfrlbpzccosQVkjL7c691Yb9y7'
client = AipOcr(APP_ID, API_KEY, SERCRET_KEY)
pdfreader_logger = common_logger.get_log('pdfreader', common_logger.LOG_DIR, 'pdfreader')
book_dir='E:/IDE/allpdf/allpdf'
img_pdf_dir='imgpdf'
text_pdf_dir='textpdf'
done_dir='donepdf'
pdf_dir='textpdf'
done_pdf_dir='done_pdf'
pdf_book_dir='pdfbook'
class SimplePdfReader(object):

    def __init__(self, pdffile):
        self.document = fitz.Document(pdffile)
        self.parent_dir = common_filer.get_parent_dir(pdffile)
        self.pdffile = pdffile
        self.filter_key_map=dict()
        self.begin_position_keys=set()
        self.menus=self.get_menus()
    
    def get_document_info(self):
        return self.document.metadata
    
    def get_pdf_book_name(self):
        book_name = self.get_document_info()['title']
        if book_name is None:
            book_name = common_filer.get_file_name(self.pdffile).replace(".pdf", "")
        return book_name
    
    def get_page_cnt(self):
        return self.document.pageCount

    def get_page_obj(self, pageno):
        return self.document[pageno]
    
    def get_page_structure_dict(self, pageno):
        return self.get_page_obj(pageno).getText("dict")
    
    def get_page_text(self, pageno):
        return self.get_page_obj(pageno).getText("text")
    
    def get_structures(self):
        structures = []
        for i in range(self.get_page_cnt()):
            structures.append(str(self.get_page_structure_dict(i)))
        return structures
    
    def get_texts(self):
        texts = []
        for i in range(self.get_page_cnt()):
            texts.append(self.get_page_text(i))
        return texts

    def get_page_tables(self, pageno):
        span_blocks = self.get_span_blocks(pageno)
        if span_blocks:
            span_dicts = self.to_pdf_span_dicts(pageno, span_blocks)
            return self.to_pdf_table_item(pageno, span_dicts)
        return []

    def get_page_links(self, pageno):
        return self.get_page_obj(pageno).getLinks()

    def get_blocks(self, pageno):
        raw_dict = self.get_page_structure_dict(pageno)
        return raw_dict['blocks']

    def get_page_images(self, pageno):
        page = self.get_page_obj(pageno)
        il = page.getImageList()
        print(len(il))
        img_list = []
        for img in il:
            xref = img[0]
            pix = self.recoverpix(img)
            if type(pix) is dict:  # we got a raw image
                ext = pix["ext"]
                imgdata = pix["image"]
                n = pix["colorspace"]
                img_list.append(PdfImage(pageno, xref, ext, imgdata, n))
            else:  # we got a pixmap
                n = pix.n
                imgdata = pix.getPNGData()
                img_list.append(PdfImage(pageno, xref, "png", imgdata, n))
        return img_list
    
    def get_images(self):
        all_list = []
        for i in range(self.get_page_cnt()):
            img_list = self.get_page_images(i)
            if img_list:
                all_list.append + img_list
        return all_list
    
    def recoverpix(self, item):
        x = item[0]  # xref of PDF image
        s = item[1]  # xref of its /SMask
        doc = self.document
        if s == 0:  # no smask: use direct image output
            return doc.extractImage(x)
        def getimage(pix):
            if pix.colorspace.n != 4:
                return pix
            tpix = fitz.Pixmap(fitz.csRGB, pix)
            return tpix
        # we need to reconstruct the alpha channel with the smask
        pix1 = fitz.Pixmap(doc, x)
        pix2 = fitz.Pixmap(doc, s)  # create pixmap of the /SMask entry
        # sanity check
        if not (pix1.irect == pix2.irect and pix1.alpha == pix2.alpha == 0 and pix2.n == 1):
            pix2 = None
            return getimage(pix1)
        pix = fitz.Pixmap(pix1)  # copy of pix1, alpha channel added
        pix.setAlpha(pix2.samples)  # treat pix2.samples as alpha value
        pix1 = pix2 = None  # free temp pixmaps
        # we may need to adjust something for CMYK pixmaps here:
        return getimage(pix)
    
    def get_menus(self):
        menus=[]
        toc = fitz.utils.getToC(self.document)
        for t in toc:
            menu_name = t[1]
            if common_tools.is_novel_chapter(menu_name):
                menus.append(t)
        return menus
    
    def get_span_image_blocks(self,pageno):
        blocks = self.get_blocks(pageno)
        image_span_blocks=[]
        for pdf_block in blocks:
            if "lines" in pdf_block:
                spans = pdf_block['lines']
                for span in spans:
                    image_span_blocks.append(["lines",span])
            if "image" in pdf_block:
                image_span_blocks.append(["image",pdf_block])
        return image_span_blocks

    def get_span_blocks(self,blocks):
        span_blocks = []
        for pdf_block in blocks:
            if "lines" in pdf_block:
                spans = pdf_block['lines']
                for span in spans:
                    span_blocks.append(span)
        return span_blocks    
    
    def get_image_blocks(self, blocks):
        image_blocks=[]
        for pdf_block in blocks:
            if "image" in pdf_block:
                image_blocks.append(pdf_block)
        return image_blocks
    
    def to_pdf_span_dicts(self, pageno, span_blocks, exclude_no=0):
        span_dicts = dict()
        for pdf_block in span_blocks:
            bbox = common_tools.to_integer_list(pdf_block['bbox'])
            span_its = self.to_pdf_span_item(pageno, pdf_block)
            pdf_key = bbox[1]
            if pdf_key in span_dicts:
                span_dicts[pdf_key] = span_dicts[pdf_key] + span_its
            else:
                span_dicts[pdf_key] = span_its
        pdf_key_list = common_tools.to_unique_list(span_dicts.keys())
        pdf_key_list.sort()
        if exclude_no > 0:
            exclude_keys = pdf_key_list[0:exclude_no]
            for exclude_key in exclude_keys:
                del span_dicts[exclude_key]
        return span_dicts

    def to_pdf_page_image(self,pageno,image_block,common_id):
        ext = image_block["ext"]
        imgdata = image_block["image"]
        n = image_block["colorspace"]
        return PdfImage(pageno, common_id, ext, imgdata, n)

    def to_pdf_image_item(self,pageno,image_block,common_id):
        print(common_id)
        pdf_image = self.to_pdf_page_image(pageno,image_block,common_id)
        bbox = common_tools.to_integer_list(image_block['bbox'])
        return PdfImg(pageno, bbox, pdf_image)

    def to_pdf_span_item(self, pageno, lines_text):
        spans = lines_text['spans']
        span_items = []
        for span_dict in spans:
            bbox = common_tools.to_integer_list(span_dict['bbox'])
            position_key = bbox[1]
            pbbox=common_tools.to_integer_list(lines_text['bbox'])
            bbox[1]=pbbox[1]
            size = span_dict['size']
            txt_val = span_dict['text']
            page_bbox_key = str(pageno)+"-"+self.to_position_key(bbox)
            if position_key >=0 and page_bbox_key not in self.filter_key_map.keys():
                self.filter_key_map[page_bbox_key]=""
                item = PdfSpan(pageno, bbox,pbbox, size, txt_val)
                span_items.append(item)
        return span_items

    def to_pdf_text(self, pageno, span_its):
        if span_its:
            text_val = self.to_pdf_text_value(span_its)
            bbox = list(span_its[0].pbbox)
            return PdfText(pageno, bbox, span_its[0].size, text_val)
        return None

    def to_pdf_link(self, pageno, span_item, page_links):
        for link in page_links:
            if self.is_same_line_position(link['from'], span_item.bbox):
                if "page" in link:
                    pdf_link_item = PdfLink(pageno, link['xref'], span_item.bbox, span_item.size, span_item.text, link['page'])
                    return pdf_link_item
                elif "uri" in link:
                    pdf_link_item = PdfLink(pageno, link['xref'], span_item.bbox, span_item.size, span_item.text, link['uri'])
                    return pdf_link_item

    def to_pdf_link_text_item(self, pageno, span_items, page_links):
        link_text_items = []
        pdf_text_item = self.to_pdf_text(pageno, span_items)
        if pdf_text_item is not None:
            self.begin_position_keys.add(pdf_text_item.bbox[0])
            pdf_link_item = self.to_pdf_link(pageno, pdf_text_item, page_links)
            if pdf_link_item is not None:
                link_text_items.append(pdf_link_item)
            else:
                for span_item in span_items:
                    pdf_link_item = self.to_pdf_link(pageno, span_item, page_links)
                    if pdf_link_item is not None:
                        link_text_items.append(pdf_link_item)
            if len(link_text_items)!=0:
                return link_text_items
            link_text_items.append(pdf_text_item)
        return link_text_items
    
    def to_pdf_table_item(self, pageno, span_dicts):
        tab_key_map = self.to_tab_cnt_key_map(span_dicts)
        pdf_key_list = self.to_pdf_key_list(span_dicts)
        tab_items = []
        for tab_cnt, pdf_keys in tab_key_map.items():
            tab_keys = [val for val in pdf_keys if val in pdf_key_list]
            if tab_cnt > 1 and tab_keys == pdf_keys:
                pdf_keys.sort()
                header_key = pdf_keys[0]
                headers = span_dicts[header_key]
                details = []
                for detail_key in pdf_keys[1:]:
                    details.append(span_dicts[detail_key])
                bbox_end = span_dicts[pdf_keys[-1]][-1].bbox
                bbox = [headers[0].bbox[0], headers[0].bbox[1], bbox_end[2], bbox_end[3]]
                pdf_tab = PdfTable(pageno, bbox, headers[0].size, headers, details)
                tab_items.append(pdf_tab)
        return tab_items

    def to_pdf_link_text_items(self,pageno,span_items):
        page_links = self.get_page_links(pageno)
        return self.to_pdf_link_text_item(pageno, span_items, page_links)
    
    def is_same_line_position(self, from_rect, positions):
        x0 = abs(int(from_rect.x0) - positions[0])
        y0 = abs(int(from_rect.y0) - positions[1])
        x1 = abs(int(from_rect.x1) - positions[2])
        y1 = abs(int(from_rect.y1) - positions[3])
        return x0 <= 3 and y0 <= 3 and x1 <= 3 and y1 <= 3

    def extract_dict_to_items(self, pageno):
        span_image_blocks = self.get_span_image_blocks(pageno)
        common_id = 0
        items = []
        for span_img_block in span_image_blocks:
            block_type = span_img_block[0]
            pdf_block = span_img_block[1]
            if block_type == "image":
                pdf_img_item = self.to_pdf_image_item(pageno, pdf_block, common_id)
                items.append(pdf_img_item)  
            if block_type == "lines":
                pdf_span_items = self.to_pdf_span_item(pageno, pdf_block)
                pdf_link_text_items = self.to_pdf_link_text_items(pageno, pdf_span_items)
                items=items+pdf_link_text_items
            common_id=common_id+1
        final_items = self.sort_pdf_items(items)
        final_item_list = []
        common_item_list = []
        for final_it in final_items:
            if common_tools.is_list(final_it):
                for final_item in final_it:
                    if final_item.item_type == "image":
                        final_item_list.append(final_item)
                        if common_item_list:
                            final_item_list.append(common_item_list)
                            common_item_list=[]
                    else:
                        common_item_list.append(final_item)
            else:
                if final_it.item_type == "image":
                    final_item_list.append(final_it)
                    if common_item_list:
                        final_item_list.append(common_item_list)
                        common_item_list=[]
                else:
                    common_item_list.append(final_it)
        if common_item_list:
            final_item_list.append(common_item_list)
        return final_item_list

    def to_pdf_final_item(self, pdf_item):
        cnt = 0
        text_val = ""
        for val in pdf_item:
            if not common_tools.is_list(val) and val.item_type == "paragraph":
                text_val = F"{text_val}{val.text}"
                cnt += 1
        if len(pdf_item) > 1 and cnt == len(pdf_item):
            pdf_item[0].text = text_val
            return pdf_item[0]
        if len(pdf_item) == 1:
            return pdf_item[0]
        return pdf_item

    def sort_pdf_items(self, items):
        y0_list = []
        y0_dict = dict()
        for pdf_item in items:
            if common_tools.is_list(pdf_item):
                y0 = pdf_item[0].index
            elif pdf_item.item_type in ["image", "paragraph", "table", "link"]:
                y0 = pdf_item.index
            y0_list.append(y0)
            if y0 not in y0_dict:
                y0_dict[y0] = []
                y0_dict[y0].append(pdf_item)
            else:
                y0_dict[y0].append(pdf_item)
        y0_unique_list = common_tools.to_unique_list(y0_list)
        y0_unique_list.sort()
        final_results = []
        for y0 in y0_unique_list:
            pdf_item = self.to_pdf_final_item(y0_dict[y0])
            final_results.append(pdf_item)
        return final_results
    
    def to_pdf_key_list(self,span_dicts):
        pdf_key_list = common_tools.to_unique_list(span_dicts.keys())
        pdf_key_list.sort()
        return pdf_key_list

    def to_tab_cnt_key_map(self, span_dicts):
        tab_key_map = dict()
        for pdf_key, span_items in span_dicts.items():
            spec_key = len(span_items)
            if spec_key in tab_key_map:
                tab_key_map[spec_key].append(pdf_key)
            else:
                tab_key_map[spec_key] = [pdf_key]
        return tab_key_map

    def to_pdf_table_order_text_items(self, pageno, span_dicts):
        page_links = self.get_page_links(pageno)
        common_items = []
        for span_items in span_dicts.values():
            pdf_link_text_items = self.to_pdf_link_text_item(pageno, span_items, page_links)
            common_items = common_items + pdf_link_text_items
        return common_items

    def add_pdf_table_into_items(self,pageno,tab_items):
        common_items = []
        for pdf_table in tab_items:
            if len(pdf_table.headers) != len(pdf_table.details) or len(pdf_table.details) == 1:
                table_header_item = self.to_pdf_text(pageno, pdf_table.headers)
                self.add_pdf_item(common_items,table_header_item)
                for pdf_table_details in pdf_table.details:
                    table_detail_item = self.to_pdf_text(pageno, pdf_table_details)
                    self.add_pdf_item(common_items,table_detail_item)
            else:
                self.add_pdf_item(common_items,pdf_table)
        return common_items

    def add_pdf_item(self,common_items,pdf_item):
        common_key_dict=dict()
        for common_item in common_items:
            position_key = self.to_position_key(common_item.bbox)
            common_key_dict[position_key]=0
        current_position_key = self.to_position_key(pdf_item.bbox)
        if current_position_key not in common_key_dict.keys():
            common_items.append(pdf_item)

    def to_position_key(self,bbox):
        return str(bbox[0])+"-"+str(bbox[1])+"-"+str(bbox[2])+"-"+str(bbox[3])
    
    def get_page_x_key(self,pageno,index):
        return str(pageno)+"-"+str(index)
    
    def is_text(self, span_its):
        cnt = 0
        for i in range(1, len(span_its)):
            span_item0 = span_its[i - 1]
            span_item1 = span_its[i]
            if span_item0.x1 == span_item1.x0:
                cnt += 1
        return cnt == len(span_its) - 1
    
    def to_pdf_text_value(self, span_its):
        text_val = ""
        for span_item in span_its:
            txt_val = span_item.text
            text_val = F"{text_val}{txt_val}"
        return text_val
        
    def get_pdf_generate_file_name(self):
        book_name = self.get_pdf_book_name()
        parent_dir = self.parent_dir
        return F"{parent_dir}/{book_name}"
    
    def write_texts_to_txt(self):
        output_name = self.get_pdf_generate_file_name()
        output_file = F"{output_name}.txt"
        file_wrtr = SimpleFileWriter(output_file)
        file_wrtr.append_lines(self.get_texts())
        file_wrtr.close()
    
    def write_image_to_parent_dir(self):
        output_name = self.get_pdf_generate_file_name()
        img_items = self.get_images()
        for img_no, img_it in enumerate(img_items):
            img_name = F"{output_name}_{img_no}.png"
            pix = fitz.Pixmap(self.document, img_it.xref)
            if pix.n < 5:
                pix.writePNG(img_name)
            else:
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG(img_name)
                pix0 = None
            pix = None

    
    def write_structure_to_txt(self):
        output_name = self.get_pdf_generate_file_name()
        output_file = F"{output_name}_struct.txt"
        file_wrtr = SimpleFileWriter(output_file)
        file_wrtr.append_lines(self.get_structures())
        file_wrtr.close()
    
    def convert_img(self):
        pdfreader_logger.info("start to convert pdf to images.")
        output_name = self.get_pdf_generate_file_name()
        common_filer.make_dirs(output_name)
        output_childs = common_filer.get_child_files(output_name)
        if len(output_childs) == self.get_page_cnt():
            return
        for pg in range(self.get_page_cnt()):
            page = self.document[pg]
            rotate = int(0)
            zoom_x =2.0
            zoom_y =2.0
            trans = fitz.Matrix(zoom_x,zoom_y).preRotate(rotate)
            pm = page.getPixmap(matrix=trans,alpha=False)
            pm.writePNG(F"{output_name}/{pg}.png")
            pdfreader_logger.info(F"{output_name}/{pg}.png")
    
    def pdf_img_to_txt(self,pg):
        output_name = self.get_pdf_generate_file_name()
        pdfreader_logger.info(F'开始识别{output_name},写入{output_name}.txt')
        wrtr = SimpleFileWriter(F'{output_name}.txt')
        png_name=F'{output_name}/{pg}.png'
        img = common_filer.get_stream_data(png_name)
        message = client.basicGeneral(img)
        if 'words_result' not in message:
            message = client.basicAccurate(img)
        pdfreader_logger.info('识别成功！')
        for text in message.get('words_result'):
            words = text.get('words')
            pdfreader_logger.info(words)
            wrtr.append_new_line(words)
        pdfreader_logger.info(F'{pg}.png')
        wrtr.close()

    def pdf_imgs_to_txt(self,from_id=None,count=None):
        if from_id is None:
            from_id = 0
        if count is None:
            count = self.get_page_cnt()
        for pg in range(from_id,count):
            self.pdf_img_to_txt(pg)
    
    def pdf_to_txt(self):
        output_name = self.get_pdf_generate_file_name()
        pdfreader_logger.info(F'开始识别{output_name},写入{output_name}.txt')
        wrtr = SimpleFileWriter(F'{output_name}.txt')
        texts = self.get_texts()
        for i,text in enumerate(texts):
            pdfreader_logger.info(text)
            wrtr.append_new_line(text)
            pdfreader_logger.info(F'page no {i}')
        wrtr.close()

    def close(self):
        self.document.close()

def start_img_pdfs_process():
    img_parent_dir = F'{book_dir}/{img_pdf_dir}'
    done_parent_dir = F'{book_dir}/{done_dir}'
    img_pdfs = common_filer.get_child_files(img_parent_dir)
    pdfreader_logger.info(img_pdfs)
    if img_pdfs:
        for img_pdf in img_pdfs:
            src_path = F'{img_parent_dir}/{img_pdf}'
            if common_filer.is_file(src_path):
                to_path = F'{done_parent_dir}/{img_pdf}'
                common_filer.move_file(src_path, to_path)
                pdfreader = SimplePdfReader(to_path)
                pdfreader.convert_img()
                pdfreader.pdf_imgs_to_txt()
    else:
        time.sleep(10)
    
def start_text_pdfs_process():
    text_parent_dir = F'{book_dir}/{text_pdf_dir}'
    done_parent_dir = F'{book_dir}/{done_dir}'
    text_pdfs = common_filer.get_child_files(text_parent_dir)
    if text_pdfs:
        for text_pdf in text_pdfs:
            src_path = F'{text_parent_dir}/{text_pdf}'
            if common_filer.is_file(src_path):
                to_path = F'{done_parent_dir}/{text_pdf}'
                common_filer.move_file(src_path, to_path)
                pdfreader = SimplePdfReader(to_path)
                pdfreader.pdf_to_txt()
    else:
        time.sleep(10)
        
def start_pdf_process():
    parent_dir = F'{book_dir}/{pdf_dir}'
    done_parent_dir = F'{book_dir}/{done_pdf_dir}'
    pdf_parent_dir=F'{book_dir}/{pdf_book_dir}'
    pdfs = common_filer.get_child_files(parent_dir)
    for pdf in pdfs:
        src_path = F'{parent_dir}/{pdf}'
        to_path=F'{done_parent_dir}/{pdf}'
        pdfreader_logger.info(src_path)
        pdfreader = SimplePdfReader(src_path)
        file_name=pdf.replace(".pdf","")
        local_pdf_dir=F'{pdf_parent_dir}/{file_name}'
        page_cnt=pdfreader.get_page_cnt()
        for i in range(page_cnt):
            page_real_index=i+1
            common_filer.make_dirs(local_pdf_dir)
            for index,item in enumerate(pdfreader.extract_dict_to_items(i)):
                convert_file_name=F"{local_pdf_dir}/{page_real_index}"
                if common_tools.is_list(item):
                    for it in item:
                        write_val_into_file(it, convert_file_name,index,False)
                else:
                    write_val_into_file(item, convert_file_name,index)
#         common_filer.move_file(src_path, to_path)

def write_val_into_file(item,convert_file_name,index,is_enter=True):
    write_file_path=F"{convert_file_name}_{index}.txt"
    filewrter=SimpleFileWriter(write_file_path)
    pdfreader_logger.info(write_file_path)
    if is_enter:
        filewrter.append_string(common_tools.output_str_from_item(item, convert_file_name, book_dir, index, "\n"))
    else:
        filewrter.append_string(common_tools.output_str_from_item(item, convert_file_name, book_dir, index, ""))
    filewrter.close()

if __name__ == "__main__":
#     pass
#     start_text_pdfs_process()
#     start_img_pdfs_process()
#     start_pdf_process()
    #'flags': 4, 'font': 'LucidaConsole' pre
    #'flags': 20, 'font': 'MicrosoftYaHei-Bold' 
#     pdf = "E:/IDE/allpdf/allpdf/pdf/自然语言处理技术入门与实战_兰红云_电子工业_2017.10.pdf"
#     pdf = "E:/IDE/allpdf/allpdf/textpdf/Perl编程语言.pdf"
    pdf = "E:/IDE/allpdf/allpdf/textpdf/Python核心编程.pdf"
    pdfreader = SimplePdfReader(pdf)
    print(pdfreader.menus)
#     pdf_output = "E:/IDE/allpdf/allpdf/pdfbook"
#     pdfreader = SimplePdfReader(pdf)
#     structures=pdfreader.get_structures()
#     key_list = []
#     for file_id,structure in enumerate(structures):
#         file_writer = SimpleFileWriter(pdf_output+"/"+str(file_id)+".txt")
#         file_writer.append_new_line(structure.replace(",",",\n"))
#         file_writer.close()
        
#     for item in pdfreader.extract_dict_to_items(3):
#         if common_tools.is_list(item):
#             for it in item:
#                 pdfreader_logger.info(it)
#         else:
#             pdfreader_logger.info(item)
#     print(pdfreader.begin_position_keys)
#     for i in range(pdfreader.get_page_cnt()):
#         for item in pdfreader.extract_dict_to_items(i):
#             if common_tools.is_list(item):
#                 for it in item:
#                     pdfreader_logger.info(it)
#             else:
#                 pdfreader_logger.info(item)
#     output_name = pdfreader.get_pdf_generate_file_name()
#     output_file = F"{output_name}_struct.txt"
#     file_wrtr = SimpleFileWriter(output_file)
#     for i in range(2):
#         struct_dict = pdfreader.get_page_structure_dict(i)
#         file_wrtr.append_new_line(str(struct_dict))
#     file_wrtr.close()
