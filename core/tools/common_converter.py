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
from tools import common_tools, common_formater
import tools.common_logger as log
import pypinyin
from Pinyin2Hanzi import DefaultDagParams,dag
import markdown
import html2text
import mistune
from deps.renderer import UbbRenderer
from const.html5tmps import HtmlTypes
from const.javatmps import JavaConst
from const.csharptmps import CSharpConst
java_const = JavaConst()
csharp_const=CSharpConst()

current_log=log.get_log('converter', log.LOG_DIR, 'converter')
h = html2text.HTML2Text()
h.ignore_links = True
h.ul_item_mark = '-'
h.body_width = 0
h.hide_strikethrough = True
html_types=HtmlTypes()
html_map_keys=html_types.html_strs

def upper2lower(str_val):
    return str_val.lower()

def lower2upper(str_val):
    return str_val.upper()

def ip2int(ip):
    ip_list=ip.split('.') #首先先把ip的组成以'.'切割然后逐次转换成对应的二进制
    result=0
    for i in range(4):  #0,1,2,3
        result=result+int(ip_list[i])*256**(3-i)
    return result

def int2ip(result_no):
    floor_list = []
    num = int(result_no)
    for i in reversed(range(4)):
        res = divmod(num,256**i)
        floor_list.append(str(res[0]))
        num = res[1]
    return '.'.join(floor_list)

def first_ones_lower(str_val,first_cnt):
    first_cnt=int(first_cnt)
    str_lines=str_val.split("\n")
    res_lines=[]
    for str_line in str_lines:
        res_lines.append(first_lower(str_line, first_cnt))
    return "\n".join(res_lines)

def first_lower(str_line,first_cnt):
    return str_line[0:first_cnt].lower()+str_line[first_cnt:]

def last_ones_lower(str_val,last_cnt):
    last_cnt=int(last_cnt)
    str_lines=str_val.split("\n")
    res_lines=[]
    for str_line in str_lines:
        res_lines.append(last_lower(str_line, last_cnt))
    return "\n".join(res_lines)

def last_lower(str_line,last_cnt):
    return str_line[0:0-last_cnt]+str_line[0-last_cnt:].lower()

def first_ones_upper(str_val,first_cnt):
    first_cnt=int(first_cnt)
    str_lines=str_val.split("\n")
    res_lines=[]
    for str_line in str_lines:
        res_lines.append(first_upper(str_line,first_cnt))
    return "\n".join(res_lines)

def first_upper(str_line,first_cnt):
    return str_line[0:first_cnt].upper()+str_line[first_cnt:]

def last_ones_upper(str_val,last_cnt):
    last_cnt=int(last_cnt)
    str_lines=str_val.split("\n")
    res_lines=[]
    for str_line in str_lines:
        res_lines.append(last_upper(str_line,last_cnt))
    return "\n".join(res_lines)

def last_upper(str_line,last_cnt):
    return str_line[0:0-last_cnt]+str_line[0-last_cnt:].upper()

def delete_first_ones(str_val,first_cnt):
    first_cnt=int(first_cnt)
    str_lines=str_val.split("\n")
    res_lines=[]
    for str_line in str_lines:
        res_lines.append(str_line[first_cnt:])
    return "\n".join(res_lines)

def delete_last_ones(str_val,last_cnt):
    last_cnt=int(last_cnt)
    str_lines=str_val.split("\n")
    res_lines=[]
    for str_line in str_lines:
        res_lines.append(str_line[0:0-last_cnt])
    return "\n".join(res_lines)

def add_first_specs(str_val,spec_str):
    str_lines=str_val.split("\n")
    res_lines=[]
    for str_line in str_lines:
        res_lines.append(spec_str+str_line)
    return "\n".join(res_lines)

def add_last_specs(str_val,spec_str):
    str_lines=str_val.split("\n")
    res_lines=[]
    for str_line in str_lines:
        res_lines.append(str_line+spec_str)
    return "\n".join(res_lines)

def chinese2pinyin(chinese_str):
    pinyin_str=''
    for i in pypinyin.pinyin(chinese_str,style=pypinyin.NORMAL):
        pinyin_str+=''.join(i)
    return pinyin_str

def pinyin2chinese(pinyin_str):
    dag_params=DefaultDagParams()
    result=dag(dag_params,list(pinyin_str.split(' ')),path_num=1,log=True)
    res_list=[]
    for item in result:
        res_list.append(''.join(item.path))
    return '\n'.join(res_list)

def wholechar2halfchar(dstring):
    n = ''
    for char in dstring:
        num = ord(char)
        if num == 0x3000:        #将全角空格转成半角空格
            num = 32
        elif 0xFF01 <=num <= 0xFF5E:       #将其余全角字符转成半角字符
            num -= 0xFEE0
        num = chr(num)
        n += num
    return n

def halfchar2wholechar(string):
    n = ''
    for char in string:
        num = ord(char)
        if(num == 32):             #半角空格转成全角
            num = 0x3000
        elif 33 <= num <= 126:
            num += 65248           #16进制为0xFEE0
        num = chr(num)
        n += num
    return n
han_list = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
unit_list = ["拾", "佰", "仟"]
fra_list = ["角", "分"]
def divide(num):
    integer = int(num)
    fraction = int(round((num-integer), 2)*100)
    return (str(integer), str(fraction))

def four_to_hanstr(num_str):
    result = ""
    num_len = len(num_str)
    for i in range(num_len):
        num = int(num_str[i])
        if i != num_len-1 and num != 0:
            result += han_list[num] + unit_list[num_len-2-i]
        else:
            result += han_list[num]
    return result
def integer_to_str(num_str):
    str_len = len(num_str)
    if str_len > 12:
        print("数字太大，翻译不了")
    elif str_len > 8:
        return four_to_hanstr(num_str[:-8]) + "亿"\
               + four_to_hanstr(num_str[-8:-4]) + "万"\
               + four_to_hanstr(num_str[-4:]) + "圆"
    elif str_len > 4:
        return  four_to_hanstr(num_str[:-4]) + "万"\
                + four_to_hanstr(num_str[-4:]) + "圆"
    else:
        return four_to_hanstr(num_str) + "圆"
def shanchu(han_str):
    shan_list = []
    for i in range(len(han_str)):
        if han_str[i] == '零':
            for j in range(i+1, len(han_str)):
                if han_str[j] == "零":
                    shan_list.append(j)
                else:
                    break
    hanlist = list(han_str)
    for i in shan_list:
        del hanlist[i]
    han_str = ""
    for i in range(len(hanlist)):
        han_str += hanlist[i]
    return han_str
def fraction_to_str(num_str):
    result = ""
    if len(num_str) == 1:
        num0 = 0
        num1 = int(num_str[0])
    else:
        num0 = int(num_str[0])
        num1 = int(num_str[1])
    if num0 != 0:
        result += han_list[num0] + fra_list[0]
        if num1 != 0:
            result += han_list[num1] + fra_list[1]
    elif num1 != 0 :
        result += han_list[num0]
        result += han_list[num1] + fra_list[1]
    else:
        result = "整"
    return result

def number2money(number_val):
    real_number=float(number_val)
    integer,fraction=divide(real_number)
    return shanchu(integer_to_str(integer))+fraction_to_str(fraction)

chinese_num = {'零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9}
chinese_amount = {'分': 0.01, '角': 0.1, '元': 1, '拾': 10, '佰': 100, '仟': 1000, '圆': 1}
    

def money2div_num(amount_str,mutiply_num,amount_float):
    amount_num = 0
    for i in chinese_amount:
        if i in amount_str:
            amount_num += chinese_num[amount_str[amount_str.index(i) - 1]] * chinese_amount[i]
    if amount_str[-1] in chinese_num.keys():
        amount_num += chinese_num[amount_str[-1]]
    amount_float += amount_num * mutiply_num
    return amount_float

def money2number(amount):
    amount_float = 0
    if '亿' in amount:
        yi = re.match(r'(.+)亿.*', amount).group(1)
        amount_float = money2div_num(yi,100000000,amount_float)
        amount = re.sub(r'.+亿', '', amount, count=1)
    if '万' in amount:
        wan = re.match(r'(.+)万.*', amount).group(1)
        amount_float = money2div_num(wan,10000,amount_float)
        amount = re.sub(r'.+万', '', amount, count=1)
    amount_yuan = 0
    for i in chinese_amount:
        if i in amount and amount[amount.index(i) - 1] in chinese_num.keys():
            amount_yuan += chinese_num[amount[amount.index(i) - 1]] * chinese_amount[i]
    amount_float += amount_yuan
    return amount_float

def markdown2html(mark_str):
    return markdown.markdown(mark_str)

def html2markdown(html_str):
    return h.handle(html_str)

def html2ubb(html_str):
    html_str=str(html_str)
    for key,value in html_map_keys.items():
        html_str=html_str.replace(key,value)
    renderer=UbbRenderer(escape=True,hard_wrap=True)
    markdown=mistune.Markdown(renderer=renderer)
    return markdown(html2markdown(html_str))

def json_to_dict(json_str):
    print(json_str)
    return json.loads(json_str)

def yaml_to_dict(yaml_str):
    return yaml.load(yaml_str)

def xml_to_dict(xml_str):
    return xmltodict.parse(xml_str)

def dict_to_json(dic_val):
    return json.dumps(dic_val)

def dict_to_yaml(dic_val):
    return yaml.dump(dic_val,allow_unicode=True)

def dict_to_xml(dict_val):
    return xmltodict.unparse(dict_val)
    
def json2yaml(json_str):
    json_data=json_to_dict(json_str)
    yaml_str=dict_to_yaml(json_data)
    return yaml_str

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

def json2prop(json_str):
    json_dict=json_to_dict(json_str)
    prop_dict={}
    dict2prop("", json_dict, prop_dict)
    prop_str=""
    for ky,vl in prop_dict.items():
        prop_str=F"{prop_str}\n{ky}={vl}"
    return prop_str
    

def dict2prop(sub_prefix,json_dict,prop_dict):
    for json_key,json_val in json_dict.items():
        sub_key=sub_prefix+"."+json_key
        if common_tools.is_base_object(json_val):
            if sub_prefix == "":
                sub_key=json_key
            prop_dict[sub_key]=json_val
        elif common_tools.is_dict(json_val):
            if sub_prefix =="":
                sub_key=json_key
            dict2prop(sub_key, json_val, prop_dict)
        elif common_tools.is_list(json_val):
            set_complex_list_to_prop_dict(sub_prefix, json_val,prop_dict)
                        
def set_complex_list_to_prop_dict(sub_prefix,json_val,prop_dict):
    for i , json_v in enumerate(json_val):
        sub_id = sub_prefix+".["+i+"]"
        if sub_prefix == "":
            sub_id = "["+i+"]"
        if common_tools.is_base_object(json_v):
            prop_dict[sub_id]=json_v
        else:
            dict2prop(sub_id, json_v, prop_dict)
    
def json2xml(json_str):
    json_dict=json_to_dict('{"xml":'+json_str+'}')
    return common_formater.format_xml(dict_to_xml(json_dict))


def set_java_entity(json_key,import_class, import_strs, property_strs, method_strs):
    prop_class=import_class
    import_classs=import_class.split(".")
    if len(import_classs)>1:
        import_strs.add(java_const.IMPORTS % (import_class))
        prop_class=import_classs[-1]
    property_strs.append(java_const.PRI_PROP % (prop_class, json_key))
    method_strs.append(java_const.SETTER % (first_upper(json_key, 1), prop_class, json_key, json_key, json_key))
    method_strs.append(java_const.GETTER % (prop_class, first_upper(json_key, 1), json_key))


def set_java_class_bodys(json_key, import_strs, property_strs, method_strs, json_val):
    if common_tools.is_time(json_val):
        set_java_entity(json_key, "java.sql.Timestamp", import_strs, property_strs, method_strs)
    elif common_tools.is_str(json_val):
        set_java_entity(json_key, "String", import_strs, property_strs, method_strs)
    if common_tools.is_int(json_val):
        set_java_entity(json_key, "Integer", import_strs, property_strs, method_strs)
    if common_tools.is_float(json_val):
        set_java_entity(json_key, "java.math.BigDecimal", import_strs, property_strs, method_strs)
    if common_tools.is_dict(json_val):
        set_java_entity(json_key, "java.util.Map", import_strs, property_strs, method_strs)
    if common_tools.is_list(json_val):
        set_java_entity(json_key, "java.util.List", import_strs, property_strs, method_strs)

def json2javaent(json_str):
    json_dict=json_to_dict(json_str)
    java_strs=[]
    for json_key in java_const.KEYS:
        if json_key not in json_dict:
            return "please input valid format as description"
    package_name = java_const.PACKAGE %(json_dict['package'])
    import_strs=set()
    property_strs=[]
    method_strs=[]
    
    for json_key,json_val in json_dict['classBody'].items():
        set_java_class_bodys(json_key, import_strs, property_strs, method_strs, json_val)
    java_strs.append(package_name)
    java_strs.append("\n".join(import_strs))
    class_obj="\n".join(property_strs) + "\n".join(method_strs)
    java_strs.append(java_const.CLASS_OBJ %(json_dict['class'],class_obj))
    return "\n\n".join(java_strs)

def set_cs_entity(json_key,prop_class, property_strs):
    property_strs.append(csharp_const.PRIVATE_PROP % (prop_class, json_key))

def set_cs_class_bodys(json_key, property_strs, json_val):
    if common_tools.is_time(json_val):
        set_cs_entity(json_key, "DateTime",  property_strs)
    elif common_tools.is_str(json_val):
        set_cs_entity(json_key, "string", property_strs)
    if common_tools.is_float(json_val):
        set_cs_entity(json_key, "decimal",  property_strs)
    if common_tools.is_int(json_val):
        set_cs_entity(json_key, "int", property_strs)
    if common_tools.is_dict(json_val):
        set_cs_entity(json_key, "Dictionary<?,?>", property_strs)
    if common_tools.is_list(json_val):
        set_cs_entity(json_key, "List<?>", property_strs)
    


def json2csent(json_str):
    json_dict=json_to_dict(json_str)
    for json_key in csharp_const.KEYS:
        if json_key not in json_dict:
            return "please input valid format as description"
    
    property_strs=[]
    
    for json_key,json_val in json_dict['classBody'].items():
        set_cs_class_bodys(json_key, property_strs, json_val)
    class_obj="\n".join(property_strs)
    class_val=csharp_const.CLASS_OBJ %(json_dict['class'],class_obj)
    cs_str = csharp_const.NAMESPACE %(json_dict['namespace'],class_val)
    return cs_str

def prop2dict(prop_str):
    prop_lines=prop_str.split('\n')
    return proplines2dict(prop_lines)

def proplines2dict(prop_lines):
    properties_dict={}
    for line in prop_lines:
        line = line.strip().replace('\n','')
        index = line.find("#")
        if index !=-1:
            line = line[0:index]
        if line.find("=")>0:
            strs=line.split("=",1)
            set_prop_key_val_to_dict(strs[0].strip(), properties_dict, strs[1].strip())
    return properties_dict

def set_prop_key_val_to_dict(str_name,dict_name,value):
    if str_name.find('.')>0:
        k = str_name.split('.')[0]
        dict_name.setdefault(k,{})
        return set_prop_key_val_to_dict(str_name[len(k)+1:], dict_name[k], value)
    else:
        dict_name[str_name]=value
        return

def get_properties_file_to_dict(properties_file):
    pro_f=open(properties_file)
    return proplines2dict(pro_f.readlines())


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

def regex2js(str1):
    js_code=F'''
    var pattern='{str1}';
    str='';
    console.log(pattern.test(str);
    '''
    return js_code

def regex2python(str1):
    py_code=F'''
    import re
    pattern=re.compile(ur'{str1}')
    str=u''
    print(pattern.search(str))
    '''
    return py_code

def regex2java(str1):
    tmp_list=["import java.util.regex.Matcher;","import java.util.regex.Pattern;","public class RegexMatches {","    public static void main(String args[]) {","        String str = "";",F'        String pattern = "{str1}";',"        Pattern r = Pattern.compile(pattern);","        Matcher m = r.matcher(str);","        System.out.println(m.matches());","    }","}"]
    java_code="\n".join(tmp_list)
    return java_code

def regex2perl(str1):
    perl_code=F'''
    #!/usr/bin/perl
    my $str="";
    if($str =~ /{str1}/)
    '''
    perl_code=perl_code+'{ print "Matched";}'
    return perl_code

def regex2bash(str1):
    bash_code=F'''
    #!/usr/bash
    test=""
    if [[ $test =~ {str1} ]];
    then
        echo "Matched"
    fi
    '''
    return bash_code

if __name__ == '__main__':
    json_str='''
{
  "rule":{
    "namespace":"strategy",
    "name":"test_exp_1496234234223400",
    "version":0,
    "last_modify_time":1434234236819000,
    "log_rate":1023300,
    "schema_version":"hello_world!"
  },
  "key":"value"
}
'''
    dict_result=json2prop(json_str)
    print(dict_result)