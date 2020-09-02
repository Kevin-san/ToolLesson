#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from django.shortcuts import render,render_to_response
from PdfWeb import services

linux_menus=services.get_menus(1)
database_menus=services.get_menus(2)
webpage_menus=services.get_menus(3)
telphone_menus=services.get_menus(4)
math_menus=services.get_menus(5)
frontkill_menus=services.get_menus(6)
lang_menus=services.get_menus(7)

linux_restfuls = services.get_restful(1, "linux")
bash_restfuls = services.get_restful(2, "bash")

def get_template_detail(book_lesson_id,api_key,menus):
    main_name=menus[book_lesson_id-1]
    return services.get_chapters(book_lesson_id, F'learn/{main_name}/{api_key}')

def index(request):
    return render(request,'index.html')

def learn_index(request):
    result = services.get_home_index()
    return render_to_response('learnindex.html',result)

def learn_linux(request,api_key):
    if api_key in linux_restfuls:
        result_dict=get_template_detail(1,api_key,linux_menus)
        return render(request,'learnbase.html',result_dict)
    return render(request, '404.html')

def learn_bash(request,api_key):
    if api_key in bash_restfuls:
        result_dict=get_template_detail(2,api_key,linux_menus)
        return render(request,'learnbase.html',result_dict)
    return render(request, '404.html')

