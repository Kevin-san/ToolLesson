#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from django.shortcuts import render,render_to_response
from PdfWeb import services,restful

menus=['linux','bash']

def index(request):
    result = services.get_home_index()
    return render_to_response('index.html',result)

def linux(request,api_key):
    if api_key in restful.get_linux_restful():
        services.get_chapters(book_lesson_id, chapter_href)
        return render(request, 'linux/%s.html' %(api_key))
    return render(request, '404.html')

def bash(request,api_key):
    if api_key in restful.get_bash_restful():
        return render(request, 'bash/%s.html' %(api_key))
    return render(request, '404.html')

