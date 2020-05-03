#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from urllib import parse
from PIL import Image
from barcode.writer import ImageWriter
import barcode
import Crypto.Cipher.AES
import Crypto.Cipher.DES3
import pyzbar.pyzbar as pyzb
import os
import base64
import hashlib
import urllib
import struct
import socket
import qrcode
import markdown
import tomd
import binascii
import math
import decimal

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

def markdown2html(mark_str):
    return markdown.markdown(mark_str)

def html2markdown(html_str):
    return tomd.Tomd(html_str).markdown

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

def ip2int(ip_str):
    return struct.unpack('!I', socket.inet_aton(ip_str)[0])

def int2ip(ip_int):
    return socket.inet_ntoa(struct.pack('!I',ip_int))

def enescape(esc_str):
    return parse.quote(esc_str.encode('unicode-escape')).replace('%5Cu','%u')

def deescape(esc_str):
    return parse.unquote(esc_str.encode().decoe('unicode-escape'))

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
    h1=hashlib.sha1(string)
    return h1.hexdigest()

def encode2base64(string):
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')

def decode2base64(string):
    return base64.b64decode(string.encode('utf-8')).decode('utf-8')

def encode2md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()

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

def encode2aes(string,key):
    aes_encode=Crypto.Cipher.AES.new(auto_fill(key),Crypto.Cipher.AES.MODE_ECB)
    return aes_encode.encrypt(auto_fill(string))

def decode2aes(string,key):
    aes_decode=Crypto.Cipher.AES.new(auto_fill(key),Crypto.Cipher.AES.MODE_ECB)
    return aes_decode.decrypt(string)

def encode2des3(string,key):
    des_coder = Crypto.Cipher.DES3.new(des_fill(key), Crypto.Cipher.DES3.MODE_ECB)
    return des_coder.encrypt(des_fill(string))

def decode2des3(string,key):
    des_coder = Crypto.Cipher.DES3.new(des_fill(key), Crypto.Cipher.DES3.MODE_ECB)
    return des_coder.decrypt(string)

def encode2rsa(string,pub_file):
    f=open(pub_file)
    pub_key=f.read()
    rsakey=RSA.importKey(pub_key)
    cipher=Cipher_pkcs1_v1_5.new(rsakey)
    return cipher.encrypt(string)

def decode2rsa(string,pri_file):
    f=open(pri_file)
    pri_key=f.read()
    rsakey = RSA.importKey(pri_key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    return cipher.decrypt(string)

def encode2url(string):
    return urllib.parse.quote(string)

def decode2url(string):
    return urllib.parse.unquote(string)