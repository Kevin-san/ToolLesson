#-*-coding:utf-8-*-
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
    url(r'^learn/index',views.learn_index, name='learn_index'),
    url(r'^tool/index',views.tool_index, name='tool_index'),
    url(r'^blog/index',views.blog_index, name='blog_index'),
    url(r'^blog/(\d+)/(\d+)/$',views.blog_list, name='blog_list'),
    url(r'^blog/article/(\d+)/$',views.blog_article, name='blog_article'),
    url(r'^blog/articles/$',views.blog_articles, name='blog_articles'),
    url(r'^blog/articleadd/$',views.blog_add, name='blog_add'),
    url(r'^blog/articleadd/submit/$',views.blog_add_submit, name='blog_add_submit'),
    url(r'^blog/articleupd/(\d+)/$',views.blog_upd, name='blog_upd'),
    url(r'^blog/articleupd/submit/$',views.blog_upd_submit, name='blog_upd_submit'),
    url(r'^blog/articledel/(\d+)/$',views.blog_del,name='blog_del'),
    url(r'^novel/index',views.novel_index,name='novel_index'),
    url(r'^novel/(\d+)/(\d+)/$',views.novel_list,name='novel_list'),
    url(r'^novel/menu/(\d+)/$',views.novel_menu,name='novel_menu'),
    url(r'^novel/content/(\d+)/(\d+)/$',views.novel_content,name='novel_content'),
    url(r'^novel/author/(\d+)/$',views.novel_author,name='novel_author'),
#     url(r'^novel/download/(\d+)/$',views.novel_download,name='novel_download'),
    url(r'^tool/funcs',views.tool_funcs,name='tool_funcs'),
    url(r'^learn/linux/([a-z]+)/$',views.learn_linux,name='learn_linux'),
    url(r'^learn/bash/([a-z]+)/$',views.learn_bash,name='learn_bash'),
    url(r'^learn/regex/([a-z]+)/$',views.learn_regex,name='learn_regex'),
    url(r'^favicon.ico$',RedirectView.as_view(url=r'static/favicon.ico')),
    url(r'^img/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'mdeditor/',include('mdeditor.urls')),
]+ static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
