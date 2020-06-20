# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''
from PyPDF2.pdf import PdfFileReader, PdfFileWriter

class SimplePdfReader(object):
    
    def __init__(self, pdf_params):
        self.pdfparams = pdf_params
        self.pdffp = open(pdf_params.pdffile, 'rb')
        self.pdfreader = PdfFileReader(self.pdffp)
        if self.pdfreader.isEncrypted:
            self.pdfreader.decrypt(pdf_params.password)

    def get_document_info(self):
        return self.pdfreader.getDocumentInfo()
    
    def get_page_obj(self, pageno):
        return self.pdfreader.getPage(pageno)
    
    def get_page_cnt(self):
        return self.pdfreader.numPages
    
    def get_page_text(self, pageno):
        return self.get_page_obj(pageno).extractText()
    
    def get_page_texts(self):
        content = ""
        for i in range(0, self.get_page_cnt()):
            content = F"{self.get_page_text(i)}\n"
        return content
    
    def split_pdf(self, from_page):
        pdfwriter = PdfFileWriter()
        for index in range(from_page, self.get_page_cnt()):
            page_obj = self.get_page_obj(index)
            pdfwriter.addPage(page_obj)
        pdfwriter.write(open(self.pdfparams.outfile, 'wb'))
    
    def close(self):
        self.pdffp.close()
