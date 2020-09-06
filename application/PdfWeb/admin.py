#-*-coding:utf-8-*-
'''
Created on 2020/09/06

@author: xcKev
'''

from django.contrib import admin

# Register your models here.

from PdfWeb import models

admin.site.register(models.User)
admin.site.register(models.UserConfirmString)