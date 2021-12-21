# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''

from spider import groupspider

def test_groupspider_download_spider_results():
    count =0
    while count < 343042:
        groupspider.download_spider_trigger_results()
        count=groupspider.insert_spider_properties(count)
        parent_downloader=groupspider.ParentDownloader("I:",groupspider.db)
        parent_downloader.get_image_spider_source_by_grps()

def test_groupspider_download_spider_missed_trigger_results():
    groupspider.download_spider_missed_trigger_results()

def test_groupspider_load_group_urls():
    groupspider.load_group_urls()

def test_groupspider_run_and_load_spider_trigger():
    groupspider.run_and_load_spider_trigger(1010)
    
def test_groupspider_download_videos():
    groupspider.download_videos("I:/Spider",groupspider.detail_attrs)
    
def test_groupspider_download_pictures():
    groupspider.download_pictures("I:/Spider", groupspider.detail_attrs)

def test_groupspider_download_novels():
    groupspider.download_novels("I:/Spider", groupspider.detail_attrs)

def test_groupspider_download_all_spiders_one_by_random_one():
    groupspider.download_all_spiders_one_by_random_one("I:/Spider", groupspider.detail_attrs)
    
if __name__ == '__main__':
#     test_groupspider_download_spider_results()
    test_groupspider_download_spider_missed_trigger_results()