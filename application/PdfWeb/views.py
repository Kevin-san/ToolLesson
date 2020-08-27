#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from django.shortcuts import render,render_to_response
from PdfWeb import services,restful

linux_menus=['linux','bash','regex','design','docker','maven','python','java','perl','cpp']
database_menus=['sql','mysql','oracle','sqlserver','sybase','sqlite','postgresql','mongodb','redis']
webpage_menus=['html','js','css']
telphone_menus=['android','kotlin','gradle']
math_menus=['math','linemath','ratemath','scoremath','theorymath']
frontkill_menus=['geek','machinelearn','deeplearn','datamine','crawler','speechsyn','voicerecog','blchain','3dmodel','unity3d']
lang_menus=['eng','jpn','chi']

def get_template_detail(book_lesson_id,api_key,menus):
    main_name=menus[book_lesson_id-1]
    return services.get_chapters(book_lesson_id, F'{main_name}/{api_key}')

def index(request):
    result = services.get_home_index()
    return render_to_response('index.html',result)

def linux(request,api_key):
    if api_key in restful.get_linux_restful():
        result_dict=get_template_detail(1,api_key,linux_menus)
        return render(request,'learnbase.html',result_dict)
    return render(request, '404.html')

def bash(request,api_key):
    if api_key in restful.get_bash_restful():
        result_dict=get_template_detail(2,api_key,linux_menus)
        return render(request,'learnbase.html',result_dict)
    return render(request, '404.html')

