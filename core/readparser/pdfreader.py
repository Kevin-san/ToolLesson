# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
import fitz
from writecreater.fileswriter import SimpleFileWriter
from tools import common_filer, common_tools
from entitys.pdfitems import PdfImage, PdfImg, PdfText, PdfLink, PdfTable, PdfSpan

class SimplePdfReader(object):

    def __init__(self, pdffile):
        self.document = fitz.Document(pdffile)
        self.parent_dir = common_filer.get_parent_dir(pdffile)
        self.pdffile = pdffile
        self.dimlimit = 100  # each image side must be greater than this
        self.relsize = 0.05  # image : pixmap size ratio must be larger than this (5%)
        self.abssize = 2048  # absolute image size limit 2 KB: ignore if smaller
    
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
        page_links = []
        for link in self.get_page_obj(pageno).getLinks():
            if "page" in link:
                page_links.append(link)
        return page_links
    
    def get_page_images(self, pageno):
        page = self.get_page_obj(pageno)
        il = page.getImageList()
        xreflist = []
        img_list = []
        for img in il:
            xref = img[0]
            if xref in xreflist:
                continue
            width = img[2]
            height = img[3]
            if min(width, height) <= self.dimlimit:
                continue
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
            if len(imgdata) <= self.abssize:
                continue
            if len(imgdata) / (width * height * n) <= self.relsize:
                continue
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

    def generate_to_objects(self):
        pass

    def get_blocks(self, pageno):
        raw_dict = self.get_page_structure_dict(pageno)
        return raw_dict['blocks']
    
    def get_span_image_blocks(self, pageno):
        blocks = self.get_blocks(pageno)
        image_blocks = []
        span_blocks = []
        for pdf_block in blocks:
            if "image" in pdf_block:
                image_blocks.append(pdf_block)
            if "lines" in pdf_block:
                span_blocks.append(pdf_block)
        return image_blocks, span_blocks
    
    def get_span_blocks(self,pageno):
        blocks = self.get_blocks(pageno)
        span_blocks = []
        for pdf_block in blocks:
            if "lines" in pdf_block:
                span_blocks.append(pdf_block)
        return span_blocks
    
    def extract_dict_to_items(self, pageno):
        items = []
        image_blocks, span_blocks = self.get_span_image_blocks(pageno)
        if image_blocks:
            for img_id, img_block in enumerate(image_blocks):
                pdf_image = self.get_page_images(pageno)[img_id]
                bbox = common_tools.to_integer_list(img_block['bbox'])
                items.append(PdfImg(pageno, bbox, pdf_image))
        if span_blocks:
            span_dicts = self.to_pdf_span_dicts(pageno, span_blocks)
            items = items + self.to_pdf_table_order_text_items(pageno, span_dicts)
        final_items = self.sort_pdf_items(items)
        return final_items
    
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

    def to_pdf_span_dicts(self, pageno, span_blocks, exclude_no=0):
        span_dicts = dict()
        for pdf_block in span_blocks:
            texts = pdf_block['lines']
            for line_text in texts:
                bbox = line_text['bbox']
                span_its = self.to_pdf_span_item(pageno, line_text)
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
    
    def to_pdf_span_item(self, pageno, lines_text):
        spans = lines_text['spans']
        span_items = []
        for span_dict in spans:
            bbox = common_tools.to_integer_list(span_dict['bbox'])
            size = span_dict['size']
            txt_val = span_dict['text']
            item = PdfSpan(pageno, bbox, size, txt_val)
            span_items.append(item)
        return span_items
    
    def to_pdf_text_item(self, pageno, span_its):
        text_val = self.to_pdf_text_value(span_its)
        bbox_end = span_its[-1]['bbox']
        bbox_start = span_its[0]['bbox']
        bbox = [bbox_start[0], bbox_start[1], bbox_end[2], bbox_end[3]]
        return PdfText(pageno, bbox, span_its[0].size, text_val)

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
    
    def to_pdf_link_items(self, pageno, span_items, page_links):
        link_items = []
        for span_item in span_items:
            link_item = self.to_pdf_link(pageno, span_item, page_links)
            if link_item is not None:
                link_items.append(link_item)
            else:
                text_item = PdfText(pageno, span_item.bbox, span_item.size, span_item.text)
                link_items.append(text_item)
        return link_items
    
    def to_pdf_pre_items(self, pageno):
        pass
    
    def to_pdf_uol_items(self, pageno):
        pass
    
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
        tab_items = self.to_pdf_table_item(pageno, span_dicts)
        if tab_items:
            common_items = common_items + tab_items
        for span_items in span_dicts.values():
            if page_links:
                common_items.append(self.to_pdf_link_items(pageno, span_items, page_links))
            elif self.is_text(span_items):
                pdf_text_item = self.to_pdf_text_item(pageno, span_items)
                common_items.append(pdf_text_item)
        return common_items        

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

    def to_pdf_link(self, pageno, span_item, page_links):
        for link in page_links:
            if self.is_same_line_position(link['from'], span_item.bbox):
                return PdfLink(pageno, link['xref'], span_item.bbox, span_item.size, span_item.text, link['page'])
    
    def is_same_line_position(self, from_rect, positions):
        x0 = abs(int(from_rect.x0) - positions[0])
        y0 = abs(int(from_rect.y0) - positions[1])
        x1 = abs(int(from_rect.x1) - positions[2])
        y1 = abs(int(from_rect.y1) - positions[3])
        if x0 <= 2 and y0 <= 2 and x1 <= 2 and y1 <= 2:
            return True
        return False
        
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
    
    def close(self):
        self.document.close()
# https://github.com/HelloGitHub-Team/HelloDjango-blog-tutorial
# https://recomm.cnblogs.com/blogpost/9472390
# https://blog.csdn.net/m0_46976252/article
# https://www.cnblogs.com/hujc/p/11273361.html
if __name__ == "__main__":
    pdf1 = "F:\EBook\Python修炼之道V1.0.pdf"
    pdf_out = "F:\EBook\Python修炼之道V1.0_test.txt"
    file_wrtr1 = SimpleFileWriter(pdf_out)
    pdfreader1 = SimplePdfReader(pdf1)
    items = pdfreader1.extract_dict_to_items(0)
    for item in items:
        file_wrtr1.append_new_line(item)
    file_wrtr1.close()
    pdf = "F:\EBook\高级Bash脚本编程指南.3.9.1 (杨春敏 黄毅 译).pdf"
    pdfreader = SimplePdfReader(pdf)
    for item in pdfreader.extract_dict_to_items(1):
        if common_tools.is_list(item):
            for it in item:
                print(it)
        else:
            print(item)
    output_name = pdfreader.get_pdf_generate_file_name()
    output_file = F"{output_name}_struct.txt"
    file_wrtr = SimpleFileWriter(output_file)
    for i in range(2):
        struct_dict = pdfreader.get_page_structure_dict(i)
        file_wrtr.append_new_line(str(struct_dict))
    file_wrtr.close()
