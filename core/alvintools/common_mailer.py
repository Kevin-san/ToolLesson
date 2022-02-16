#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/10

@author: xcKev
'''

import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def get_smtp_object(mail_host='',mail_user='',mail_pass=''):
    if mail_host == '' and mail_user == '' and mail_pass == '':
        return smtplib.SMTP('localhost')
    smtp_obj=smtplib.SMTP()
    smtp_obj.connect(mail_host,25)
    smtp_obj.login(mail_user, mail_pass)
    return smtp_obj

def get_message(content,sender,receivers,subject,text_format='plain',encoding='utf-8'):
    message=MIMEMultipart()
    message['From']=sender
    message['To']=','.join(receivers)
    message['Subject']=Header(subject,encoding)
    message_text=MIMEText(content,text_format,encoding)
    message.attach(message_text)
    return message

def add_attach(message,attach_paths,encoding='utf-8'):
    for attach_path in attach_paths:
        file_name=os.path.basename(attach_path)
        att=MIMEText(open(attach_path,'rb').read(),'base64',encoding)
        att['Content-Type']='application/octet-stream'
        att['Content-Disposition']=F'attachment; filename="{file_name}"'
        message.attach(att)
    
def add_html_image(message,image_paths,image_ids):
    for index,image_path in enumerate(image_paths):
        msg_image=MIMEImage(open(image_path,'rb').read())
        msg_image.add_header('Content-ID', F'<{image_ids[index]}>')
        message.attach(msg_image)

def send_mail(sender,receivers,content,subject,text_format,encoding,attachs):
    smtp_obj=get_smtp_object()
    message=get_message(content, sender, receivers, subject, text_format, encoding)
    add_attach(message, attachs, encoding)
    smtp_obj.sendmail(sender, receivers, message.as_string().encoding('ascii'))
    
