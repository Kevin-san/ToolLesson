#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''

from PdfWeb.models import BookLessonType,BookLesson,Chapter,Content,ImageContent,CommonRules
from PdfWeb.entitys import HomeInfoItem

def get_book_lesson_type_by_id(book_lesson_type_id):
    return BookLessonType().objects.get(pk=book_lesson_type_id,DeleteFlag=0)

def get_book_lesson_by_id(book_lesson_id):
    return BookLesson().objects.get(pk=book_lesson_id,DeleteFlag=0)

def get_content_by_id(content_id):
    return Content().objects.get(pk=content_id,DeleteFlag=0)

def get_chapter_by_id(chapter_id):
    return Chapter().objects.get(pk=chapter_id,DeleteFlag=0)

def get_image_content_by_id(image_id):
    return ImageContent.objects.get(pk=image_id,DeleteFlag=0)

def get_chapter_by_href(href):
    return Chapter.objects.filter(Href=href,DeleteFlag=0).order_by('ChapterNo')

def get_book_lesson_type_info():
    return BookLessonType.objects.filter(DeleteFlag=0)

def get_book_lesson_info(book_lesson_type_id):
    return BookLesson.objects.filter(BookLessonType_Id=book_lesson_type_id,DeleteFlag=0)

def get_chapter_infos(book_lesson_id):
    return Chapter.objects.filter(BookLesson_Id=book_lesson_id,DeleteFlag=0).order_by('ChapterNo')

def get_content_infos(chapter_id):
    return Content.objects.filter(Chapter_Id=chapter_id,DeleteFlag=0).order_by('OrderIndex')
    
def get_image_content_infos(image_id):
    return ImageContent.objects.filter(Id=image_id,DeleteFlag=0)

def get_book_lesson_image_info(book_lesson_type_id):
    book_lessons=get_book_lesson_info(book_lesson_type_id)
    book_lesson_image_list=[]
    for book_lesson in book_lessons:
        image_content = get_image_content_infos(book_lesson.ImageContent_Id)
        home_info_item=HomeInfoItem(book_lesson,image_content[0])
        book_lesson_image_list.append(home_info_item)
    return book_lesson_image_list

def get_common_rules():
    return CommonRules.objects.filter(DeleteFlag=0)

def get_common_rules_by_type(rule_type):
    return CommonRules.objects.filter(TypeKey=rule_type,DeleteFlag=0)

def get_common_rules_by_type_and_rule(rule_type,rules):
    return CommonRules.objects.filter(TypeKey=rule_type,Rules=rules,DeleteFlag=0)
