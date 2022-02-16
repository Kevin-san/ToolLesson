#-*- encoding:UTF-8 -*-
'''
Created on 2021/12/8

@author: xcKev
'''

import PdfWeb.constant as const
from django.shortcuts import render,redirect

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