#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''

from PdfWeb.models import BookLessonTypeInfo,BookLessonInfo,ChapterInfo,ContentInfo,ImageContentInfo,\
    CommonRulesInfo
from PdfWeb.entitys import HomeInfoItem


def get_book_lesson_type_info():
    return BookLessonTypeInfo.objects.filter(DeleteFlag=0)

def get_book_lesson_info(book_lesson_type_id):
    return BookLessonInfo.objects.filter(LessonTypeId=book_lesson_type_id,DeleteFlag=0)

def get_chapter_infos(book_lesson_id):
    return ChapterInfo.objects.filter(BookLessonId=book_lesson_id,DeleteFlag=0).order_by('ChapterNo')

def get_chapter_by_href(href):
    return ChapterInfo.objects.filter(Href=href,DeleteFlag=0).order_by('ChapterNo')

def get_content_infos(chapter_id):
    return ContentInfo.objects.filter(ChapterId=chapter_id,DeleteFlag=0).order_by('OrderIndex')
    
def get_image_content_infos(image_id):
    return ImageContentInfo.objects.filter(Id=image_id,DeleteFlag=0)

def get_book_lesson_image_info(book_lesson_type_id):
    book_lessons=get_book_lesson_info(book_lesson_type_id)
    book_lesson_image_list=[]
    for book_lesson in book_lessons:
        image_content = get_image_content_infos(book_lesson.ImageId)
        home_info_item=HomeInfoItem(book_lesson,image_content[0])
        book_lesson_image_list.append(home_info_item)
    return book_lesson_image_list

def get_common_rules():
    return CommonRulesInfo.objects.filter(DeleteFlag=0).order_by('Id')

def get_common_rules_by_type(rule_type):
    return CommonRulesInfo.objects.filter(TypeKey=rule_type,DeleteFlag=0).order_by('Id')

def get_common_rules_by_type_and_rule(rule_type,rules):
    return CommonRulesInfo.objects.filter(TypeKey=rule_type,Rules=rules,DeleteFlag=0).order_by('Id')
