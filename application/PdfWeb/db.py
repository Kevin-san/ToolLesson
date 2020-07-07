#-*-coding:utf-8-*-
'''
Created on 2019/12/28

@author: xcKev
'''

from PdfWeb.models import BookLessonTypeInfo,BookLessonInfo,ChapterInfo,ContentInfo,ImageContentInfo
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
    return ImageContentInfo.objects.filter(ImageId=image_id,DeleteFlag=0)

def get_book_lesson_image_info(book_lesson_type_id):
    book_lessons=get_book_lesson_info(book_lesson_type_id)
    book_lesson_image_list=[]
    for book_lesson in book_lessons:
        image_content = get_image_content_infos(book_lesson.ImageId)
        home_info_item=HomeInfoItem(book_lesson,image_content)
        book_lesson_image_list.add(home_info_item)
    return book_lesson_image_list

def get_menus(typekey):
    return MenuInfo.objects.filter(MenuType=typekey,DeleteFlag=0)

def get_menu_indexs(typekey):
    return LessonMenuIndexInfo.objects.filter(Type=typekey,DeleteFlag=0)

def get_image(img_name):
    return ImageInfo.objects.filter(ImgKey=img_name,DeleteFlag=0)

def get_details(parent_key):
    return DetailsInfo.objects.filter(ParentKey=parent_key,DeleteFlag=0)

def get_child_details(parent_key):
    return DetailsInfo.objects.filter(ParentKey=parent_key,DeleteFlag=0,ParentFlag=0)

def get_children_detail(parent_key):
    return DetailsInfo.objects.filter(ParentKey__contains=parent_key,DeleteFlag=0,ParentFlag=0)

def get_parent_detail(parent_key):
    key_list=parent_key.split('-')[:-1]
    key_val=key_list[-1]
    typekey='-'.join(key_list[:-1])
    tag_type=key_val.split(':')[0]
    tag_order=key_val.split(':')[1]
    return DetailsInfo.objects.filter(ParentKey=typekey,Type=tag_type,OrderIndex=tag_order,DeleteFlag=0)
