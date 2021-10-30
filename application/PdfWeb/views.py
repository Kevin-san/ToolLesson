#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''
from django.shortcuts import render,redirect
from PdfWeb import services,forms,settings,db,current_log
import PdfWeb.constant as const
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

blog_categorys_map = dict(db.get_blog_category_type_info().values_list('CategoryId','CategoryName'))
tag_categorys_map = dict(db.get_blog_tag_category_type_info().values_list('CategoryId','CategoryName'))

def create_dict_base_on_keys_form(keys_list,form_data):
    dict_result={}
    for dict_key in keys_list:
        dict_result[dict_key] = form_data.cleaned_data[dict_key]
    return dict_result
def create_dict_from_keys_form(keys_list,int_keys,form_data):
    dict_result={}
    for dict_key in keys_list:
        dict_result[dict_key] = form_data.cleaned_data[dict_key]
    for dict_key in int_keys:
        dict_result[dict_key] = int(form_data.cleaned_data[dict_key])
        if dict_key == 'CategoryId':
            dict_result['CategoryId'] = int(form_data.cleaned_data[dict_key])
            dict_result['CategoryName'] = blog_categorys_map[dict_result['CategoryId']]
        elif dict_key == 'TagId':
            dict_result['TagId'] = int(form_data.cleaned_data[dict_key])
            dict_result['TagName'] = tag_categorys_map[dict_result['TagId']]
    return dict_result
    

def get_template_detail(book_lesson_id,api_key,menus):
    main_name=menus[book_lesson_id-1]
    return services.get_chapters(book_lesson_id, F'learn/{main_name}/{api_key}')

def is_not_login(request):
    return not request.session.get(const.IS_LOGIN_KEY, None)

def render_no_access(request):
    content=const.NO_ACCESS
    return render(request,const.INDEX_HTML,locals())

def index(request):
    content=services.get_home_index()
    if is_not_login(request):
        content=const.NO_ACCESS
    return render(request,const.INDEX_HTML,locals())

def userprofile(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        user_id = request.session['user_id']
        user = services.get_user_by_id(user_id)
        edit_form = forms.EditUserForm(initial={'Id':user.Id,'Name':user.Name,'Email':user.Email,'Sex':user.Sex,'Logo':user.Logo,'Detail':user.Detail})
        result = {'edit_form':edit_form}
        return render(request,const.USER_PROFILE_HTML,result)

def useredit(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        edited_form=forms.EditUserForm(request.POST)
        if edited_form.is_valid():  # 获取数据
            user_id = request.session['user_id']
            org_user = services.get_user_by_id(user_id)
            username = edited_form.cleaned_data['Name']
            email = edited_form.cleaned_data['Email']
            sex = edited_form.cleaned_data['Sex']
            logo = org_user.Logo
            if edited_form.cleaned_data['Logo']:
                logo = edited_form.cleaned_data['Logo']
            detail = edited_form.cleaned_data['Detail']
            same_name_user = services.get_user_by_name(username)
            same_email_user = services.get_user_by_email(email)
            if same_name_user.Id != user_id:  # 用户名唯一
                message = const.EXIST_USER
                return redirect(const.USER_PROFILE_URL)
            if same_email_user.Id != user_id:  # 邮箱地址唯一
                message = const.EXIST_EMAIL
                return redirect(const.USER_PROFILE_URL)
            if email != org_user.Email or username != org_user.Name or sex != org_user.Sex or logo != org_user.Logo or detail != org_user.Detail:
                services.update_user(org_user.Id,username,email,sex,detail,logo)
                user = services.get_user_by_id(org_user.Id)
                request.session[const.IS_LOGIN_KEY] = True
                request.session['user_id'] = user.Id
                request.session['user_name'] = user.Name
                request.session['user_logo'] = user.Logo
        return redirect(const.USER_PROFILE_URL)

def login(request):
    if request.session.get(const.IS_LOGIN_KEY,None):
        return redirect(const.INDEX_URL)
    if request.method == const.METHOD_POST:
        login_form = forms.UserForm(request.POST)
        message = const.CHECK_VALUE
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = services.get_user_by_name(username)
            if user is None:
                message = const.NO_USER
                return render(request, const.LOGIN_HTML, locals())
            if user.DeleteFlag ==1:
                message = const.NO_CONFIRM
                return render(request, const.LOGIN_HTML, locals())
            if check_password(password,user.Password):
                request.session[const.IS_LOGIN_KEY] = True
                request.session['user_id'] = user.Id
                request.session['user_name'] = user.Name
                request.session['user_logo'] = user.Logo.url
                return redirect(const.INDEX_URL)
            else:
                message = const.WRONG_PWD
        return render(request, const.LOGIN_HTML, locals())
    login_form = forms.UserForm()
    return render(request, const.LOGIN_HTML, locals())

def logout(request):
    if is_not_login(request):
        # 如果本来就未登录，也就没有登出一说
        return redirect(const.INDEX_URL)
    request.session.flush()
    return redirect(const.INDEX_URL)

def register(request):
    if not is_not_login(request):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect(const.INDEX_URL)
    if request.method == const.METHOD_POST:
        register_form = forms.RegisterForm(request.POST,request.FILES)
        message = const.CHECK_VALUE
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            logo = register_form.cleaned_data['logo']
            detail = register_form.cleaned_data['detail']
            permission = register_form.cleaned_data['permissions']
            same_name_user = services.get_user_by_name(username)
            same_email_user = services.get_user_by_email(email)
            if password1 != password2:  # 判断两次密码是否相同
                message = const.DIFF_PWD
                return render(request, const.REG_HTML, locals())
            if same_name_user:  # 用户名唯一
                message = const.EXIST_USER
                return render(request, const.REG_HTML, locals())
            if same_email_user:  # 邮箱地址唯一
                message = const.EXIST_EMAIL
                return render(request, const.REG_HTML, locals())
            new_user=services.new_user(username, password1, email, sex,detail,logo, permission)
            send_email(email,services.make_confirm_string(new_user))
            return redirect(const.LOGIN_URL)  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, const.REG_HTML, locals())

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
        message = const.INVALID_MSG
        return render(request, const.CONFIRM_HTML, locals())
    c_time = confirm.c_time
    now = datetime.datetime.utcnow()
    confirm_time = c_time + datetime.timedelta(settings.CONFIRM_DAYS)
    if now > confirm_time:
        services.delete_by_confirm(confirm)
        message = const.OLD_EMAIL
        return render(request, const.CONFIRM_HTML, locals())
    else:
        services.update_user_by_confirm(confirm)
        message = const.CONFIRM_LOGIN
        return render(request, const.CONFIRM_HTML, locals())

def blog_index(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_blog_home_index()
        return render(request,const.BLOG_INDEX_HTML,result)

def blog_list(request,category_id,page_no):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_blog_home_list(category_id,page_no)
        return render(request,const.BLOG_INDEX_HTML,result)
    
def blog_article(request,article_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        current_log.info(article_id)
        result = services.get_blog_article(article_id)
        result['action'] = const.DETAIL_ACTION
        result['comment_form'] = forms.CommentForm()
        return render(request,const.BLOG_BASE_HTML,result)
    
def blog_articles(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        author_id = request.session['user_id']
        result = services.get_blog_article_info(author_id)
        result['action'] = const.DETAIL_LIST_ACTION
        return render(request,const.BLOG_BASE_HTML,result)

def blog_add(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        author_id = request.session['user_id']
        result=services.get_blog_article_info(author_id)
        result['action'] = const.ADD_ACTION
        result['form'] = forms.ArticleForm()
        return render(request,const.BLOG_BASE_HTML,result)

def blog_del(request,article_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        author_id = request.session['user_id']
        services.del_blog_article_by_id(article_id)
        return redirect('/blog/articles/'+author_id)

def blog_upd(request,article_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result=services.get_blog_article(article_id)
        article  = result['article']
        article_form = forms.ArticleForm(initial={'Id':article.Id,'AuthorId':article.AuthorId,'Title':article.Title,'Synopsis':article.Synopsis,'CategoryId':article.CategoryId,'TagId':article.TagId,'Type':article.Type,'Original':article.Original,'Content':article.Content})
        result['action'] = const.UPD_ACTION
        result['form']=article_form
        return render(request,const.BLOG_BASE_HTML,result)

def blog_add_submit(request):
    article_form = forms.ArticleForm(request.POST,request.FILES)
    article_keys = ['Title','Synopsis','CategoryId','TagId','Type','Original','Content']
    int_keys = ['CategoryId','TagId','Type','Original']
    if article_form.is_valid():
        article_dict = create_dict_from_keys_form(article_keys,int_keys, article_form)
        author_dict = {'AuthorId':request.session['user_id'],'AuthorName':request.session['user_name']}
        real_dict = dict(article_dict,**author_dict)
        article=services.ins_blog_article(real_dict)
        return blog_article(request, article.Id)
    return blog_add(request)

def blog_upd_submit(request):
    article_form = forms.ArticleForm(request.POST,request.FILES)
    if article_form.is_valid():
        article_dict = services.get_blog_article(int(article_form.cleaned_data['Id']))
        article = article_dict['article']
        article.Synopsis = article_form.cleaned_data['Synopsis']
        article.CategoryId = int(article_form.cleaned_data['CategoryId'])
        article.CategoryName = blog_categorys_map[article.CategoryId]
        article.TagId = int(article_form.cleaned_data['TagId'])
        article.TagName = tag_categorys_map[article.TagId]
        article.Type = int(article_form.cleaned_data['Type'])
        article.Original = int(article_form.cleaned_data['Original'])
        article.Content = article_form.cleaned_data['Content']
        article.Title = article_form.cleaned_data['Title']
        services.upd_blog_article(article)
        return blog_article(request, article.Id)
    return blog_upd(request, article.Id)

def book_index(request,book_type):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_book_home_index(book_type)
        return render(request,const.BOOK_INDEX_HTML,result)

def book_list(request,book_type,category_id,page_no):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_book_list(book_type,category_id,page_no)
        return render(request,const.BOOK_INDEX_HTML,result)

def book_menu(request,book_type,book_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_book_menu_info(book_type,book_id)
        return render(request,const.BOOK_BASE_HTML,result)

def book_section(request,book_type,book_id,section_order_no,max_section_order_no):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_book_section_info(book_type,book_id,section_order_no,max_section_order_no)
        return render(request,const.BOOK_BASE_HTML,result)

def book_author(request,book_type,book_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_book_infos_by_author(book_type,book_id)
        return render(request,const.BOOK_BASE_HTML,result)

def book_menuadd(request,book_type):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result=dict()
        result['action'] = const.ADD_ACTION
        result['item']='book'
        result['book_type']=book_type
        result['form'] = forms.LearnForm()
        if book_type =='novel':
            result['form'] = forms.NovelForm()
        result['book_id']=0
        return render(request,const.BOOK_BASE_HTML,result)

def book_menudel(request,book_type,book_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result=services.del_book_by_id(book_type,book_id)
        return render(request,const.BOOK_INDEX_HTML,result)

def book_menuupd(request,book_type,book_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_book_info(book_type,book_id)
        book=result['book']
        result['form']=forms.LearnForm(initial={'Id':book.Id,'BookName':book.BookName,'Description':book.Description,'Author':book.Author,'ImageContent':book.ImageContent,'CategoryId':book.CategoryId})
        if book_type=='novel':
            result['form']=forms.NovelForm(initial={'Id':book.Id,'BookName':book.BookName,'Description':book.Description,'Author':book.Author,'ImageContent':book.ImageContent,'CategoryId':book.CategoryId})
        result['action']=const.UPD_ACTION
        result['item']='book'
        result['book_id']=book.Id
        return render(request, const.BOOK_BASE_HTML, result)

def get_book_form(request, book_type):
    book_form = forms.LearnForm(request.POST, request.FILES)
    if book_type == 'novel':
        book_form = forms.NovelForm(request.POST, request.FILES)
    return book_form

def book_add_submit(request,book_type,book_id):
    book_form = get_book_form(request, book_type)
    book_keys = ['BookName','Description','Author','ImageContent','CategoryId']
    if book_form.is_valid():
        book_dict = create_dict_base_on_keys_form(book_keys,book_form)
        book=services.ins_book(book_dict)
        return book_menu(request, book_type,book.Id)
    return book_menuadd(request,book_type)

def book_upd_submit(request,book_type,book_id):
    book_form = get_book_form(request, book_type)
    if book_form.is_valid():
        book_id=int(book_form.cleaned_data['Id'])
        result = services.get_book_info(book_type, book_id)
        book = result['book']
        book.BookName = book_form.cleaned_data['BookName']
        book.Description = book_form.cleaned_data['Description']
        book.Author = book_form.cleaned_data['Author']
        book.ImageContent = book_form.cleaned_data['ImageContent']
        book.CategoryId = book_form.cleaned_data['CategoryId']
        book.UpdateUser=request.session['user_name']
        services.upd_book(book)
        return book_menu(request,book_type, book_id)
    return book_menuupd(request,book_type,book_id)

def book_sectionadd(request,book_type,book_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result=services.get_book_info(book_type, book_id)
        section_no=0
        order_no=services.get_max_book_section_order_no(book_id)+1
        result['action'] = const.ADD_ACTION
        result['item']='section'
        result['booksec_id']=book_id
        result['form'] = forms.SectionForm(initial={'BookId':book_id,'OrderNo':order_no,'SectionNo':section_no})
        return render(request,const.BOOK_BASE_HTML,result)

def book_sectiondel(request,book_type,section_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result=services.del_section_by_id(book_type,section_id)
        return render(request,const.BOOK_BASE_HTML,result)

def book_sectionupd(request,book_type,section_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result=services.get_section_info(book_type,section_id)
        section=result['section']
        result['action'] = const.UPD_ACTION
        result['item']='section'
        result['booksec_id']=section_id
        result['form'] = forms.SectionForm(initial={'Id':section.Id,'BookId':section.BookId,'OrderNo':section.OrderNo,'SectionNo':section.SectionNo,'ChapterName':section.ChapterName,'Content':section.Content})
        return render(request,const.BOOK_BASE_HTML,result)

def section_add_submit(request,book_type,book_id):
    section_form = forms.SectionForm(request.POST,request.FILES)
    section_keys = ['BookId','OrderNo','SectionNo','ChapterName','Content']
    if section_form.is_valid():
        section_dict = create_dict_base_on_keys_form(section_keys,section_form)
        section=services.ins_section(section_dict)
        book=services.get_book_info(book_type, book_id)['book']
        book.MaxSectionId=section.OrderNo
        book.MaxSectionName=section.ChapterName
        services.upd_book(book)
        max_section_order_no=services.get_max_book_section_order_no(book_id)
        return book_section(request, book_type, book_id,section.OrderNo, max_section_order_no)
    return book_sectionadd(request,book_type,book_id)

def section_upd_submit(request,book_type,section_id):
    section_form = forms.SectionForm(request.POST,request.FILES)
    if section_form.is_valid():
        section = services.get_book_section(int(section_form.cleaned_data['Id']))
        section.OrderNo = int(section_form.cleaned_data['OrderNo'])
        section.SectionNo = int(section_form.cleaned_data['SectionNo'])
        section.ChapterName = section_form.cleaned_data['ChapterName']
        section.Content = section_form.cleaned_data['Content']
        services.upd_section(section)
        book_id=section.BookId
        max_section_order_no=services.get_max_book_section_order_no(book_id)
        max_section = services.get_book_section_by_order_no(book_id,max_section_order_no)
        book=services.get_book_info(book_type, book_id)['book']
        book.MaxSectionId=max_section.OrderNo
        book.MaxSectionName=max_section.ChapterName
        services.upd_book(book)
        return book_section(request, book_type, book_id,section.OrderNo,max_section_order_no)
    return book_sectionupd(request, book_type, section_id)

def media_index(request,media_type):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_media_home_index(media_type)
        return render(request,const.MEDIA_INDEX_HTML,result)

def media_list(request,media_type,category_id,page_no):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_media_list(media_type,category_id,page_no)
        return render(request,const.MEDIA_INDEX_HTML,result)

def media_content(request,media_type,media_id,order_no):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_media_content(media_type,media_id,order_no)
        return render(request,const.MEDIA_BASE_HTML,result)

def tool_index(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_tool_home_index()
        return render(request,const.TOOL_INDEX_HTML,result)

def tool_funcs(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result_str = services.get_tool_func(request.POST.get('tool'),request.POST.get('method'),request.POST.get('inputarea'),request.POST.get('passkey'));
        result_dict = {'outputarea':result_str};
        return HttpResponse(json.dumps(result_dict))



def novel_index(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_novel_home_index()
        return render(request,const.NOVEL_INDEX_HTML,result)

def novel_list(request,novel_source_id,page_no):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_novel_home_list(novel_source_id, page_no)
        return render(request,const.NOVEL_INDEX_HTML,result)
    
def novel_menu(request,novel_item_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_novel_menu_info(novel_item_id)
        return render(request,const.NOVEL_BASE_HTML,result)

def novel_content(request,novel_property_id,last_upd_content_ord_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_novel_content_info(novel_property_id, last_upd_content_ord_id)
        return render(request,const.NOVEL_BASE_HTML,result)

def novel_author(request,novel_item_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_novel_infos_by_author(novel_item_id)
        return render(request,const.NOVEL_BASE_HTML,result)

def image_index(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_image_home_index()
        return render(request,const.IMAGE_INDEX_HTML,result)

def image_list(request,image_source_id,page_no):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_image_home_list(image_source_id, page_no)
        return render(request,const.IMAGE_INDEX_HTML,result)

def image_content(request,item_id):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_image_content_info(item_id)
        return render(request,const.IMAGE_BASE_HTML,result)

def learn_index(request):
    if is_not_login(request):
        return render_no_access(request)
    else:
        result = services.get_learn_home_index()
        return render(request,const.LEARN_INDEX_HTML,result)
    

def learn_linux(request,api_key):
    if api_key in linux_restfuls:
        if is_not_login(request):
            return render_no_access(request)
        else:
            result_dict=get_template_detail(1,api_key,linux_menus)
            return render(request,const.LEARN_BASE_HTML,result_dict)
    return render(request, const.ERROR_HTML)

def learn_bash(request,api_key):
    if api_key in bash_restfuls:
        if is_not_login(request):
            return render_no_access(request)
        else:
            result_dict=get_template_detail(2,api_key,linux_menus)
            return render(request,const.LEARN_BASE_HTML,result_dict)
    return render(request, const.ERROR_HTML)

def learn_regex(request,api_key):
    if api_key in regex_restfuls:
        if is_not_login(request):
            return render_no_access(request)
        else:
            result_dict=get_template_detail(3,api_key,linux_menus)
            return render(request,const.LEARN_BASE_HTML,result_dict)
    return render(request, const.ERROR_HTML)



