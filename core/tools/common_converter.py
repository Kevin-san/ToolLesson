#-*- encoding:UTF-8 -*-
'''
Created on 2019/12/28

@author: xcKev
'''

import json
import yaml
import xmltodict
import configparser
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfdevice import TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter,HTMLConverter,TextConverter
from pdfminer.layout import LAParams
import fitz
import re
from tools import common_tools
import tools.common_logger as log
current_log=log.get_log('converter', '/temp', 'converter')


def json_to_dict(json_str):
    return json.loads(json_str)

def yaml_to_dict(yaml_str):
    return yaml.load(yaml_str)

def xml_to_dict(xml_str):
    return xmltodict.parse(xml_str)

def dict_to_json(dic_val):
    return json.dumps(dic_val)

def dict_to_yaml(dic_val):
    return yaml.dump(dic_val)

def dict_to_xml(dict_val):
    return xmltodict.unparse(dict_val)
    
def json2yaml(json_str):
    json_data=json_to_dict(json_str)
    return yaml.dump(json_data)

def yaml2json(yaml_str):
    yaml_data=yaml_to_dict(yaml_str)
    return json.dumps(yaml_data)

def json2csv(json_str,split_char=","):
    json_data=json_to_dict(json_str)
    if common_tools.is_list_and_ge_len(json_data,1):
        csv_list=[]
        csv_headers = list(json_data[0])
        csv_list.append(split_char.join(csv_headers))
        for item_dict in json_data:
            line_str=common_tools.get_csv_str_from_dict(csv_headers,split_char,item_dict)
            csv_list.append(line_str)
        return "\n".join(csv_list)
    else:
        current_log.info(F"please input list json format! : {json_str}")
        return ""

def csv2json(csv_str,split_char=",",header_index=0):
    json_list=[]
    csv_list=csv_str.split("\n")
    if common_tools.is_list_and_ge_len(csv_list,2):
        dict_keys=common_tools.get_csv_headers(csv_list,header_index,split_char)
        for idx in range(header_index+1,len(csv_list)):
            csv_str = csv_list[idx]
            json_dict=common_tools.get_dict_from_csv_str(dict_keys,split_char,csv_str)
            json_list.append(json_dict)
        return json.dumps(json_list)
    else:
        current_log.info(F"please input list csv format! : {csv_str}")
        return ""

def get_properties_file_to_dict(properties_file):
    pro_f=open(properties_file)
    properties_dict={}
    for line in pro_f.readlines():
        line = line.strip().replace('\n','')
        index = line.find("#")
        if index !=-1:
            line = line[0:index]
        if line.find("=")>0:
            strs=line.split("=",1)
            to_properties_dict(strs[0].strip(), properties_dict, strs[1].strip())
    return properties_dict

def to_properties_dict(str_name,dict_name,value):
    if str_name.find('.')>0:
        k = str_name.split('.')[0]
        dict_name.setdefault(k,{})
        return to_properties_dict(str_name[len(k)+1:], dict_name[k], value)
    else:
        dict_name[str_name]=value
        return
#c#
def get_ini_file_to_dict(ini_file):
    cfg=configparser.ConfigParser()
    cfg.read(ini_file, encoding="utf8")
    ini_dic=dict(cfg._sections)
    for k in ini_dic:
        ini_dic[k]=dict(ini_dic[k])
    return ini_dic

def get_json_file_to_dict(json_file):
    json_f=open(json_file,'r')
    loaded_json=json.load(json_f)
    return loaded_json
    
def get_yaml_file_to_dict(yaml_file):
    yaml_f=open(yaml_file,'r')
    loaded_yaml=yaml.load(yaml_f)
    return loaded_yaml
            
def init_params():
    rsrcmgr=PDFResourceManager(caching=True)
    laparams=LAParams()
    return rsrcmgr,laparams

def get_device(pdf_params,outfp,rsrcmgr,laparams):
    if pdf_params.outtype =='txt':
        return TextConverter(rsrcmgr,outfp,laparams=laparams,imagewriter=None)
    elif pdf_params.outtype =='html':
        return HTMLConverter(rsrcmgr,outfp,scale=1,layoutmode='normal',laparams=laparams,imagewriter=None,debug=0)
    elif pdf_params == 'xml':
        return XMLConverter(rsrcmgr,outfp,laparams=laparams,imagewriter=None,stripcontrol=False)
    elif pdf_params=='tag':
        return TagExtractor(rsrcmgr,outfp)
    return TextConverter(rsrcmgr,outfp,laparams=laparams,imagewriter=None)

def pdf2file(rsrcmgr,device,fp,outfp,password):
    pagenos=set()
    maxpages=0
    rotation=0
    interpreter=PDFPageInterpreter(rsrcmgr,device)
    for page in PDFPage.get_pages( fp, pagenos, maxpages, password, caching=True, check_extractable=True):
        page.rotate=(page.rotate+rotation)%360
        interpreter.process_page(page)
    device.close()
    outfp.close()
    return 

def pdf2any(pdf_params):
    fp=open(pdf_params.pdffile,'rb')
    outfp=open(pdf_params.outfile,'w',encoding=pdf_params.encoding)
    rsrcmgr,laparams=init_params()
    device=get_device(pdf_params, outfp, rsrcmgr, laparams)
    pdf2file(rsrcmgr, device, fp, outfp, pdf_params.password)

def pdf2pic(pdf_params):
    check_xo=r"/Type(?= */XObject)"
    check_im=r"/Subtype(?= */Image)"
    doc = fitz.Document(pdf_params.pdffile)
    imgcount=0
    len_xref=doc._getXrefLength()
    for i in range(1,len_xref):
        text=doc._getXrefString(i)
        if not re.search(check_xo,text) or not re.search(check_im,text):
            continue
        imgcount+=1
        pix=fitz.Pixmap(doc,i)
        if pix.n < 5:
            try:
                pix.writePNG(F"{pdf_params.imgdir}/img_{imgcount}.png")
            except RuntimeError:
                pix0 = fitz.Pixmap(fitz.csRGB,pix)
                pix0.writePNG(F"{pdf_params.imgdir}/img_{imgcount}.png")
                pix0 = None
        else:
            pix0 = fitz.Pixmap(fitz.csRGB,pix)
            pix0.writePNG(F"{pdf_params.imgdir}/img_{imgcount}.png")
            pix0 = None
    return

def htmlspec2str(str1):
    return str1.replace("&nbsp;"," ").replace("&lt;","<").replace("&gt;",">").replace("\t","    ")

def str2htmlspec(str1):
    return str1.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;")