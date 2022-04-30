#-*- encoding:UTF-8 -*-
'''
Created on 2021/12/8

@author: xcKev
'''

import PdfWeb.constant as const
from django.shortcuts import render,redirect
import re 

def auth_required(func):
    def inner_auth_required(request,*args,**kwargs):
        if not request.session.get(const.IS_LOGIN_KEY, None):
            content=const.NO_ACCESS
            return render(request,const.INDEX_HTML,locals())
        return func(request,*args,**kwargs)
    return inner_auth_required

def login_required(func):
    def inner_login_required(request,*args,**kwargs):
        if request.session.get(const.IS_LOGIN_KEY,None):
            return redirect(const.INDEX_URL)
        return func(request,*args,**kwargs)
    return inner_login_required

def group_role_required(func):
    def inner_group_role_required(request,*args,**kwargs):
        current_url = "/"+request.path+"/"
        conv_current_url = re.sub(r'\d+', "[num]", current_url)
        valid_urls = request.session['user_valid_urls']
        for valid_url in valid_urls:
            if conv_current_url.startswith(valid_url):
                return func(request,*args,**kwargs)
        return render(request,const.INDEX_HTML,locals())
    return inner_group_role_required