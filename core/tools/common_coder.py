#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,DES3,ARC4,DES
from Crypto.Util.Padding import pad
from urllib import parse
from PIL import Image
from barcode.writer import ImageWriter
import barcode
import pyzbar.pyzbar as pyzb
import hmac
import os
import base64
import hashlib

import qrcode
import binascii
import math
import decimal

typemap={"thunder":("AA","ZZ"),"flashget":("[FLASHGET]","[FLASHGET]"),"qqdl":("","")}
def get_num(num, out=''):
    num = decimal.Decimal(num)
    codes = "abcdefghjkmnpqrstuvwxyz23456789ABCDEFGHJKMNPQRSTUVWXYZ"
    if num > 53:
        key = num % 54
        num = math.floor(num / 54) - 1
        return get_num(num, codes[int(key)] + out)
    else:
        return codes[int(num)] + out

def num2shortcd(num):
    return get_num(num)

def shortcd2num(shortcd):
    codes = "abcdefghjkmnpqrstuvwxyz23456789ABCDEFGHJKMNPQRSTUVWXYZ"
    num = 0
    num = decimal.Decimal(num)
    i = len(shortcd)
    for char in shortcd:
        i -= 1
        pos = codes.find(char)
        num += (54 ** i) * (pos + 1)
    num -= 1
    return int(num)

def create_barcode(str_val,img_directory,barcodeing):
    EAN = barcode.get_barcode_class(barcodeing)
    ean = EAN(str_val,writer=ImageWriter())
    return ean.save(img_directory)

def b64encode_img(file_path):
    file_sc = open(file_path,'rb')
    return str(base64.b64encode(file_sc.read()))

def char2hex(char_str):
    return binascii.b2a_hex(char_str.encode("utf-8"))

def hex2char(code_str):
    return binascii.a2b_hex(code_str).decode("utf-8")

def str2sixteenth(string):
    return char2hex(string).decode()

def sixteenth2str(string):
    return hex2char(string)

def str_q2b(ustring):
    ss=[]
    for st in ustring:
        rstring = ""
        for uchar in st:
            inside_code = ord(uchar)
            if inside_code ==12288:
                inside_code=32
            elif (inside_code>=65281 and inside_code <= 65374):
                inside_code-=65248
            rstring+=chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

def str_b2q(ustring):
    ss=[]
    for st in ustring:
        rstring=""
        for uchar in st:
            inside_code = ord(uchar)
            if inside_code ==32:
                inside_code=12288
            elif (inside_code>=33 and inside_code<=126):
                inside_code+=65248
            rstring+=chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

def tenth2anyth(result_str,tenth_num,source_list):
    if tenth_num==0:
        return result_str
    len_num = len(source_list)
    first_int = tenth_num%len_num
    second_int = tenth_num-first_int
    if tenth_num < len_num:
        first_int=tenth_num
    if first_int==len_num:
        first_int=0
    result_str = source_list[first_int]+result_str
    return tenth2anyth(result_str, second_int//len_num, source_list)

def anyth2tenth(from_str,from_source_list):
    sourc_str=''.join(list(reversed(from_str)))
    tenth_num=0
    cnt=0
    for s_it in sourc_str:
        index=from_source_list.index(s_it)
        val_num = len(from_source_list)**cnt
        tenth_num=tenth_num+index*val_num
        cnt=cnt+1
    return tenth_num

def anyth2anyth(from_str,from_source_list,to_source_list):
    tenth_num = anyth2tenth(from_str, from_source_list)
    return tenth2anyth('', tenth_num, to_source_list)



def qrcode2str(img_path):
    if not os.path.exists(img_path):
        raise FileExistsError(img_path)
    return pyzb.decode(Image.open(img_path),symbols=[pyzb.ZBarSymbol.QRCODE])

def str2qrcode(data_str,img_path):
    img=qrcode.make(data=data_str)
    img.save(img_path)

def hex2rgb(hex_color):
    rgb_color=[(hex_color >> 16) & 0xff,(hex_color >> 8) & 0xff,hex_color & 0xff]
    return rgb_color

def rgb2hex(rgb_color):
    r,g,b=rgb_color
    return (r<<16)+(g<<8)+b

def enescape(esc_str):
    return parse.quote(esc_str.encode('unicode-escape')).replace('%5Cu','%u')

def deescape(esc_str):
    return parse.unquote(esc_str.encode().decode('unicode-escape'))

def bin2oct(string_num):
    return oct(int(string_num,2))
    
def bin2dec(string_num):
    return int(string_num,2)
    
def bin2hex(string_num):
    return hex(int(string_num,2))
    
def oct2bin(string_num):
    return bin(int(string_num,8))
    
def oct2dec(string_num):
    return int(string_num,8)

def oct2hex(string_num):
    return hex(int(string_num,8))

def dec2bin(string_num):
    return bin(int(string_num,10))

def dec2oct(string_num):
    return oct(int(string_num,10))

def dec2hex(string_num):
    return hex(int(string_num,10))

def hex2bin(string_num):
    return bin(int(string_num,16))

def hex2oct(string_num):
    return oct(int(string_num,16))

def hex2dec(string_num):
    return int(string_num,16)

def keep_decimal(num,n):
    return round(num, n)

def add_header_zero(num,n):
    return str(num).zfill(n)

def encode2sha1(string):
    return encode2hashlib(string, "sha1")

def encode2md5(string):
    return encode2hashlib(string, "md5")

def encode2sha224(string):
    return encode2hashlib(string, "sha224")

def encode2sha256(string):
    return encode2hashlib(string, "sha256")

def encode2sha384(string):
    return encode2hashlib(string, "sha384")

def encode2sha512(string):
    return encode2hashlib(string, "sha512")

def encode2hashlib(string,digestmod):
    return hashlib.new(digestmod, string.encode('utf-8')).hexdigest()

def encode2hmacsha1(string,key):
    return encode2hmacstr(string, key, "sha1")

def encode2hmacmd5(string,key):
    return encode2hmacstr(string, key, "md5")

def encode2hmacsha224(string,key):
    return encode2hmacstr(string, key, "sha224")

def encode2hmacsha256(string,key):
    return encode2hmacstr(string, key, "sha256")

def encode2hmacsha384(string,key):
    return encode2hmacstr(string, key, "sha384")

def encode2hmacsha512(string,key):
    return encode2hmacstr(string, key, "sha512")

def encode2hmacstr(string,key,digestmod):
    return hmac.new(key.encode('utf-8'), string.encode('utf-8'), digestmod=digestmod).hexdigest()

def encode2base64(string):
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')

def decode2base64(string):
    return base64.b64decode(string.encode('utf-8')).decode('utf-8')

def encode2download(url,downloadtype):
    typeval=typemap[downloadtype]
    encodeurl=encode2base64(typeval[0]+url+typeval[1])
    finalurl=F"{downloadtype}://{encodeurl}"
    if downloadtype == "flashget":
        finalurl=F"{finalurl}==&abc"
    return finalurl

def encode2thunder(url):
    return encode2download(url, "thunder")

def encode2flashget(url):
    return encode2download(url, "flashget")

def encode2qqdl(url):
    return encode2download(url, "qqdl")

def decode2thunder(url):
    return decode2download(url, "thunder")

def decode2flashget(url):
    return decode2download(url, "flashget")

def decode2qqdl(url):
    return decode2download(url, "qqdl")

def decode2download(url,downloadtype):
    typevals=typemap[downloadtype]
    encodeurl=url.replace(F"{downloadtype}://","",1)
    if downloadtype == "flashget":
        encodeurl=encodeurl[encodeurl.lastindex("==&abc"):]
    strbuffer=decode2base64(encodeurl)
    return strbuffer[len(typevals[0]):0-len(typevals[1])]

def custom_pad(text):
    text = text.encode()
    result = len(text) %8
    if ( result != 0): #当字节数不是8的倍数时，用\0字节补全
        text = text + (b'\0'*(16-result))
    return text

def auto_fill(x):
    if len(x) <= 32:
        while len(x) not in [16,24,32]:
            x+=" "
        return x.encode()
    else:
        raise "密匙长度不能大于32位"

def des_fill(x):
    if len(x) > 24:
        raise "密钥长度不能大于等于24位！"
    else:
        while len(x) < 16:
            x += " "
        return x.encode()

def rand_func(no):
    b_arrays=[b'H',b'H',b'H']
    return b_arrays[no]

def encode2des(string,passkey):
    byte_data=pad(string.encode(),24)
    des=DES.new(pad(passkey.encode(),8), DES.MODE_ECB)
    return str(base64.encodebytes(des.encrypt(byte_data)),encoding='utf8').replace('\n','')

def decode2des(string,passkey):
    des=DES.new(pad(passkey.encode(),8), DES.MODE_ECB)
    decrypted_text=des.decrypt(base64.decodebytes(bytes(string,encoding='utf8'))).decode('utf8')
    return decrypted_text[:-ord(decrypted_text[-1])]

def encode2aes(string,key):
    byte_data=pad(string.encode(),32)
    aes_encode=AES.new(auto_fill(key),AES.MODE_ECB)
    return str(base64.encodebytes(aes_encode.encrypt(byte_data)), encoding='utf8').replace('\n', '')

def decode2aes(string,key):
    aes_decode=AES.new(auto_fill(key),AES.MODE_ECB)
    decrypted_text = aes_decode.decrypt(base64.decodebytes(bytes(string, encoding='utf8'))).decode("utf8")  # 解密
    decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
    return decrypted_text

def encode2des3(string,key):
    byte_data=pad(string.encode(),32)
    des_coder = DES3.new(des_fill(key), DES3.MODE_ECB)
    return str(base64.encodebytes(des_coder.encrypt(byte_data)), encoding='utf8').replace('\n', '')

def decode2des3(string,key):
    des_coder = DES3.new(des_fill(key), DES3.MODE_ECB)
    decrypted_text = des_coder.decrypt(base64.decodebytes(bytes(string, encoding='utf8'))).decode("utf8")  # 解密
    decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
    return decrypted_text

def encode2rsa(string,pub_key):
    rsakey=RSA.importKey(pub_key)
    cipher=Cipher_pkcs1_v1_5.new(rsakey,rand_func)
    return base64.b64encode(cipher.encrypt(string.encode())).decode()

def decode2rsa(string,pri_key):
    rsakey = RSA.importKey(pri_key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey,rand_func)
    return cipher.decrypt(base64.b64decode(string), 'ERROR').decode('utf-8')

def encode2rc4(string,passkey):
    rc41=ARC4.new(passkey.encode())
    encrypted = rc41.encrypt(string.encode())
    return base64.b64encode(encrypted).decode()


def decode2rc4(string,passkey):
    rc41=ARC4.new(passkey.encode())
    return rc41.decrypt(base64.b64decode(string)).decode()

def encodeurl(str_url):
    str_vals=str_url.split("?",2)
    return str_vals[0]+"?"+encode2url(str_vals[1])

def decodeurl(str_url):
    str_vals=str_url.split("?",2)
    return str_vals[0]+"?"+decode2url(str_vals[1])

def encode2url(string):
    return parse.quote(string)

def decode2url(string):
    return parse.unquote(string)

def unicode2str(string):
    strs=[]
    for i_str in string:
        conv_str=hex(ord(i_str))[2:]
        if len(conv_str) ==4:
            strs.append('\\\\u'+conv_str)
        else:
            strs.append(i_str)
    return ''.join(strs)

def str2unicode(string):
    return string.encode('utf-8').decode('unicode_escape')

def ascii2str(string):
    sourcelist=string.split("&#")
    results=""
    for ord_it in sourcelist[1:]:
        results+=chr(int(ord_it[:-1]))
    return results

def str2ascii(string):
    results=[]
    for char_it in string:
        results.append("&#"+str(ord(char_it))+";")
    return "".join(results)

def base2n(num, b):
    return ((num == 0) and "0") or (base2n(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"[num % b])

def sec2any(num_str):
    results=[]
    real_num = int(num_str,2)
    results.append(F"二进制:{num_str}")
    results.append("四进制:"+str(base2n(real_num,4)))
    results.append("八进制:"+str(bin2oct(num_str)))
    results.append("十进制:"+str(bin2dec(num_str)))
    results.append("十六进制:"+str(bin2hex(num_str)))
    results.append("三十二进制:"+str(base2n(real_num,32)))
    results.append("六十四进制:"+str(base2n(real_num,64)))
    return "\n".join(results)

def four2any(num_str):
    results=[]
    real_num=int(num_str,4)
    results.append("二进制:"+str(base2n(real_num,2)))
    results.append(F"四进制:{num_str}")
    results.append("八进制:"+str(base2n(real_num,8)))
    results.append("十进制:"+str(real_num))
    results.append("十六进制:"+str(base2n(real_num,16)))
    results.append("三十二进制:"+str(base2n(real_num,32)))
    results.append("六十四进制:"+str(base2n(real_num,64)))
    return "\n".join(results)

def eight2any(num_str):
    results=[]
    real_num=int(num_str,8)
    results.append("二进制:"+str(oct2bin(num_str)))
    results.append("四进制:"+str(base2n(real_num,4)))
    results.append(F"八进制:{num_str}")
    results.append("十进制:"+str(oct2dec(num_str)))
    results.append("十六进制:"+str(oct2hex(num_str)))
    results.append("三十二进制:"+str(base2n(real_num,32)))
    results.append("六十四进制:"+str(base2n(real_num,64)))
    return "\n".join(results)

def ten2any(num_str):
    results=[]
    real_num=int(num_str)
    results.append("二进制:"+str(dec2bin(num_str)))
    results.append("四进制:"+str(base2n(real_num,4)))
    results.append("八进制:"+str(dec2oct(num_str)))
    results.append(F"十进制:{num_str}")
    results.append("十六进制:"+str(dec2hex(num_str)))
    results.append("三十二进制:"+str(base2n(real_num,32)))
    results.append("六十四进制:"+str(base2n(real_num,64)))
    return "\n".join(results)

def sixteen2any(num_str):
    results=[]
    real_num=int(num_str,16)
    results.append("二进制:"+str(hex2bin(num_str)))
    results.append("四进制:"+str(base2n(real_num,4)))
    results.append("八进制:"+str(hex2oct(num_str)))
    results.append("十进制:"+str(hex2dec(num_str)))
    results.append(F"十六进制:{num_str}")
    results.append("三十二进制:"+str(base2n(real_num,32)))
    results.append("六十四进制:"+str(base2n(real_num,64)))
    return "\n".join(results)
def thirtytwo2any(num_str):
    results=[]
    real_num=int(num_str,32)
    results.append("二进制:"+str(base2n(real_num,2)))
    results.append("四进制:"+str(base2n(real_num,4)))
    results.append("八进制:"+str(base2n(real_num,8)))
    results.append("十进制:"+str(real_num))
    results.append("十六进制:"+str(base2n(real_num,16)))
    results.append(F"三十二进制:{num_str}")
    results.append("六十四进制:"+str(base2n(real_num,64)))
    return "\n".join(results)
def sixtyfour2any(num_str):
    results=[]
    real_num=int(num_str,64)
    results.append("二进制:"+str(base2n(real_num,2)))
    results.append("四进制:"+str(base2n(real_num,4)))
    results.append("八进制:"+str(base2n(real_num,8)))
    results.append("十进制:"+str(real_num))
    results.append("十六进制:"+str(base2n(real_num,16)))
    results.append("三十二进制:"+str(base2n(real_num,32)))
    results.append(F"六十四进制:{num_str}")
    return "\n".join(results)