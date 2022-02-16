#-*- encoding:UTF-8 -*-
"""alvin_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include
import PdfWeb.views as views
from django.conf import settings
from django.conf.urls.static import static,serve
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index',views.index,name='index'),
    url(r'^login',views.login,name='login'),
    url(r'^register',views.register,name='register'),
    url(r'^useredit',views.useredit,name='useredit'),
    url(r'^userprofile',views.userprofile,name='userprofile'),
    url(r'^logout',views.logout,name='logout'),
    url(r'^confirm/$', views.user_confirm,name='confirm'),
    url(r'^captcha', include('captcha.urls')),
    url(r'^tool/index',views.tool_index, name='tool_index'),
    url(r'^tool/funcs',views.tool_funcs,name='tool_funcs'),
    url(r'^blog/index',views.blog_index, name='blog_index'),
    url(r'^blog/(\d+)/(\d+)/$',views.blog_list, name='blog_list'),
    url(r'^blog/article/(\d+)/$',views.blog_article, name='blog_article'),
    url(r'^blog/articles/$',views.blog_articles, name='blog_articles'),
    url(r'^blog/articleadd/$',views.blog_add, name='blog_add'),
    url(r'^blog/articleadd/submit/$',views.blog_add_submit, name='blog_add_submit'),
    url(r'^blog/articleupd/(\d+)/$',views.blog_upd, name='blog_upd'),
    url(r'^blog/articleupd/submit/$',views.blog_upd_submit, name='blog_upd_submit'),
    url(r'^blog/articledel/(\d+)/$',views.blog_del,name='blog_del'),
    url(r'^blog/download/(\d+)/$',views.blog_download,name='blog_download'),
    url(r'^(blog|novel|learn|audio|image|video)/comment/ins/(\d+)/$',views.comment_add_submit,name='comment_add_submit'),
    url(r'^(blog|novel|learn|audio|image|video)/comment/del/(\d+)/$',views.comment_del,name='comment_del'),
    url(r'^(novel|learn)/book/index',views.book_index,name='book_index'),
    url(r'^(novel|learn)/book/(\d+)/(\d+)/$',views.book_list,name='book_list'),
    url(r'^(novel|learn)/book/menu/(\d+)/$',views.book_menu,name='book_menu'),
    url(r'^(novel|learn)/book/menuadd/$',views.book_menuadd,name='book_menuadd'),
    url(r'^(novel|learn)/book/menuupd/(\d+)/$',views.book_menuupd,name='book_menuupd'),
    url(r'^(novel|learn)/book/menuupd/(\d+)/submit/$',views.book_upd_submit,name='book_upd_submit'),
    url(r'^(novel|learn)/book/menudel/(\d+)/$',views.book_menudel,name='book_menudel'),
    url(r'^(novel|learn)/book/menuadd/(\d+)/submit/$',views.book_add_submit,name='book_add_submit'),
    url(r'^(novel|learn)/book/sectionadd/(\d+)/$',views.book_sectionadd,name='book_sectionadd'),
    url(r'^(novel|learn)/book/sectionadd/(\d+)/submit/$',views.section_add_submit,name='section_add_submit'),
    url(r'^(novel|learn)/book/sectiondel/(\d+)/$',views.book_sectiondel,name='book_sectiondel'),
    url(r'^(novel|learn)/book/sectionupd/(\d+)/$',views.book_sectionupd,name='book_sectionupd'),
    url(r'^(novel|learn)/book/sectionupd/(\d+)/submit/$',views.section_upd_submit,name='section_upd_submit'),
    url(r'^(novel|learn)/book/section/(\d+)/(\d+)/(\d+)/$',views.book_section,name='book_section'),
    url(r'^(novel|learn)/book/author/(\d+)/$',views.book_author,name='book_author'),
    url(r'^(novel|learn)/book/download/(\d+)/$',views.book_download,name='book_download'),
    url(r'^(novel|learn)/book/upload/$',views.book_upload,name='book_upload'),
    url(r'^(image|audio|video)/media/index',views.media_index,name='media_index'),
    url(r'^(image|audio|video)/media/(\d+)/(\d+)/$',views.media_list,name='media_list'),
    url(r'^(image|audio|video)/media/content/(\d+)/(\d+)/$',views.media_content,name='media_content'),
    url(r'^(image|audio|video)/media/download/(\d+)/$',views.media_download,name='media_download'),
    url(r'^(image|audio|video)/media/upload/$',views.media_upload,name='media_upload'),
    url(r'^(image|audio|video)/media/upload/submit/$',views.media_upload_submit,name='media_upload_submit'),
    url(r'^favicon.ico$',RedirectView.as_view(url=r'static/favicon.ico')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'mdeditor/',include('mdeditor.urls')),
]+ static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
