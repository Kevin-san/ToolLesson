# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''

from alvinspider import groupspider,parentdownloader
from alvintools import get_remote_folder
from alvintools import common_filer

remote_dir = get_remote_folder()

def test_groupspider_download_spider_results():
    count =0
    while count < 343042:
        count=groupspider.insert_spider_properties(count)
        parent_downloader=parentdownloader.ParentDownloader(remote_dir,groupspider.db)
        parent_downloader.get_image_spider_source_by_grps()
        groupspider.download_spider_trigger_results()
        groupspider.download_spider_missed_trigger_results()
        common_filer.merge_ts_and_to_mp4(remote_dir+"/Spider/Hider/Video/亚洲无码")
        

def test_groupspider_download_spider_missed_trigger_results():
    groupspider.download_spider_missed_trigger_results()

def test_groupspider_load_group_urls():
    groupspider.load_group_urls()

def test_groupspider_run_and_load_spider_trigger():
    groupspider.run_and_load_spider_trigger(1010)
    
def test_groupspider_download_videos():
    groupspider.download_videos(remote_dir+"/Spider",groupspider.detail_attrs)
    
def test_groupspider_download_pictures():
    groupspider.download_pictures(remote_dir+"/Spider", groupspider.detail_attrs)

def test_groupspider_download_novels():
    groupspider.download_novels(remote_dir+"/Spider", groupspider.detail_attrs)

def test_groupspider_download_all_spiders_one_by_random_one():
    groupspider.download_all_spiders_one_by_random_one(remote_dir+"/Spider", groupspider.detail_attrs)
    
if __name__ == '__main__':
#     test_groupspider_download_spider_results()
    test_groupspider_download_spider_missed_trigger_results()