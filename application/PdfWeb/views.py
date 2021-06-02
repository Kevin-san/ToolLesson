#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from django.shortcuts import render,redirect
from PdfWeb import services,forms,settings
import datetime
from django.contrib.auth.hashers import check_password
from django.http.response import HttpResponse
import json

linux_menus=services.get_menus(11)
database_menus=services.get_menus(12)
webpage_menus=services.get_menus(13)
telphone_menus=services.get_menus(14)
math_menus=services.get_menus(15)
frontkill_menus=services.get_menus(16)
lang_menus=services.get_menus(17)

linux_restfuls = services.get_restful(1, "linux")
bash_restfuls = services.get_restful(2, "bash")
regex_restfuls = services.get_restful(3, "regex")

def get_template_detail(book_lesson_id,api_key,menus):
    main_name=menus[book_lesson_id-1]
    return services.get_chapters(book_lesson_id, F'learn/{main_name}/{api_key}')

def index(request):
    content=services.get_home_index()
    if not request.session.get('is_login',None):
        content="你还没有权限访问任何画面！请登录"
    return render(request,'index.html',locals())

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index')

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = services.get_user_by_name(username)
            if user is None:
                message = "用户不存在！"
                return render(request, 'login.html', locals())
            if user.DeleteFlag ==1:
                message = "该用户还未通过邮件确认！"
                return render(request, 'login.html', locals())
            if check_password(password,user.Password):
                request.session['is_login'] = True
                request.session['user_id'] = user.Id
                request.session['user_name'] = user.Name
                return redirect('/index')
            else:
                message = "密码不正确！"
        return render(request, 'login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index")
    request.session.flush()
    return redirect("/index")

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            detail = register_form.cleaned_data['detail']
            permission = register_form.cleaned_data['permissions']
            same_name_user = services.get_user_by_name(username)
            same_email_user = services.get_user_by_email(email)
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'
                return render(request, 'register.html', locals())
            if same_email_user:  # 邮箱地址唯一
                message = '该邮箱地址已被注册，请使用别的邮箱！'
                return render(request, 'register.html', locals())
            new_user=services.new_user(username, password1, email, sex,detail, permission)
            send_email(email,services.make_confirm_string(new_user))
            return redirect('/login')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())

def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自www.alvin.com的确认邮件'
    text_content = '欢迎访问www.alvin.com，这里是Alvin站点，专注于各种知识分享！'
    html_content = '<p>欢迎注册<a href="https://{}/confirm/?code={}" target="blank">www.alvin.com</a>，这里是Alvin的站点，专注于各种知识的分享！</p>'.format('127.0.0.1:8000',code)
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    confirm = services.get_confirm(code)
    if confirm is None:
        message = '无效的确认请求!'
        return render(request, 'confirm.html', locals())
    c_time = confirm.c_time
    now = datetime.datetime.utcnow()
    confirm_time = c_time + datetime.timedelta(settings.CONFIRM_DAYS)
    if now > confirm_time:
        services.delete_by_confirm(confirm)
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'confirm.html', locals())
    else:
        services.update_user_by_confirm(confirm)
        message = '感谢确认，请使用账户登录！'
        return render(request, 'confirm.html', locals())

def blog_index(request):
    if not request.session.get('is_login',None):
        content="你还没有权限访问任何画面！请登录"
        return render(request,'index.html',locals())
    else:
        result = services.get_blog_home_index() 
        return render(request,'blogindex.html',result)

def blog_list(request,category_id,page_no):
    if not request.session.get('is_login',None):
        content="你还没有权限访问任何画面！请登录"
        return render(request,'index.html',locals())
    else:
        result = services.get_blog_home_list(category_id,page_no)
        return render(request,'blogindex.html',result)
    
def blog_article(request,article_id):
    if not request.session.get('is_login',None):
        content="你还没有权限访问任何画面！请登录"
        return render(request,'index.html',locals())
    else:
        result = services.get_blog_article(article_id)
        return render(request,'blogbase.html',result)
    
    
def tool_index(request):
    if not request.session.get('is_login',None):
        content="你还没有权限访问任何画面！请登录"
        return render(request,'index.html',locals())
    else:
        result = services.get_tool_home_index()
        return render(request,'toolindex.html',result)

def tool_funcs(request):
    if not request.session.get('is_login',None):
        content="你还没有权限访问任何画面！请登录"
        return render(request,'index.html',locals())
    else:
        result_str = services.get_tool_func(request.POST.get('tool'),request.POST.get('method'),request.POST.get('inputarea'),request.POST.get('passkey'));
        result_dict = {'outputarea':result_str};
        return HttpResponse(json.dumps(result_dict))

def learn_index(request):
    if not request.session.get('is_login',None):
        content="你还没有权限访问任何画面！请登录"
        return render(request,'index.html',locals())
    else:
        result = services.get_learn_home_index()
        return render(request,'learnindex.html',result)
    

def learn_linux(request,api_key):
    if api_key in linux_restfuls:
        if not request.session.get('is_login',None):
            content="你还没有权限访问任何画面！请登录"
            return render(request,'index.html',locals())
        else:
            result_dict=get_template_detail(1,api_key,linux_menus)
            return render(request,'learnbase.html',result_dict)
    return render(request, '404.html')

def learn_bash(request,api_key):
    if api_key in bash_restfuls:
        if not request.session.get('is_login',None):
            content="你还没有权限访问任何画面！请登录"
            return render(request,'index.html',locals())
        else:
            result_dict=get_template_detail(2,api_key,linux_menus)
            return render(request,'learnbase.html',result_dict)
    return render(request, '404.html')

def learn_regex(request,api_key):
    if api_key in regex_restfuls:
        if not request.session.get('is_login',None):
            content="你还没有权限访问任何画面！请登录"
            return render(request,'index.html',locals())
        else:
            result_dict=get_template_detail(3,api_key,linux_menus)
            return render(request,'learnbase.html',result_dict)
    return render(request, '404.html')

def blog_detail(request,id):
    pass

def blog_add(request,id):
    pass

def blog_upd(request,id):
    pass