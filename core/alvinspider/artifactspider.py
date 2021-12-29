#-*-coding:utf-8-*-
'''
Created on 2019/6/10

@author: xcKev
'''
import alvintools.common_tools as common
from alvintools import common_filer
import alvinspider.common_spider as common_spider
import os

class ArtifactsSpider():
    def __init__(self,artifactory,local_home,user,password):
        self.artifactory=artifactory
        self.local_home=common.get_home_path(local_home)
        self.user=user
        self.password=password
    
    def get_artifact_info(self,artifact_url):
        artifact_url=common.get_home_path(artifact_url)
        html=common_spider.get_response_text(artifact_url, self.user, self.password)
        a_list=common_spider.get_beautifulsoup_from_html(html,'a')
        a_href_list=[]
        a_name_list=[]
        for a_item in a_list:
            if a_item == '../':
                continue
            a_name_list.append(a_item.text)
            a_href = a_item.get('href')
            href_url = common_spider.get_url(artifact_url, a_href)
            a_href_list.append(href_url)
        return a_name_list,a_href_list
    
    def get_artifact_infos(self,a_name_list,a_href_list):
        if common.is_file(a_name_list):
            return a_name_list,a_href_list
        new_href_list=[]
        new_name_list=[]
        for index,a_name in enumerate(a_name_list):
            arti_url=a_href_list[index]
            child_name_list,child_href_list=self.get_artifact_info(arti_url)
            if len(child_name_list) ==0:
                new_name_list.append(a_name)
                new_href_list.append(arti_url)
                continue
            for index in range(0,len(child_name_list)):
                child_name=child_name_list[index]
                child_href=child_href_list[index]
                new_name_list.append(a_name+child_name)
                new_href_list.append(child_href)
        return self.get_artifact_infos(new_name_list, new_href_list)
    
    def get_download_artifacts_infos(self):
        a_name_list,a_href_list=self.get_artifact_info(self.artifactory)
        final_a_name_list,final_a_href_list=self.get_artifact_infos(a_name_list, a_href_list)
        return final_a_name_list,final_a_href_list
    
    def write_artifacts_info_into_artitext(self,a_name_list):
        dir_list,file_list=common.get_directory_file_list(a_name_list)
        common_filer.make_dirs(self.local_home)
        arti_f=open(self.local_home+'artifacts.txt','w+')
        for index,dir_name in enumerate(dir_list):
            arti_f.write(dir_name+'='+file_list[index]+'\n')
        arti_f.close()
    
    def download_files_from_url(self,a_name_list,a_href_list):
        for index,path_name in enumerate(a_name_list):
            directory,file_name=common.get_dir_file(path_name)
            common_filer.make_dirs(self.local_home+directory)
            download_url=a_href_list[index]
            res=common_spider.get_response(download_url, self.user, self.password)
            file_w=open(self.local_home+file_name,'wb')
            file_w.write(res.content)
            file_w.close()
    
    def download_artifacts(self):
        final_a_name_list,final_a_href_list=self.get_download_artifacts_infos()
        self.write_artifacts_info_into_artitext(final_a_name_list)
        self.download_files_from_url(final_a_name_list,final_a_href_list)
    
    @staticmethod
    def download_artifacts_service():
        artifact_url=os.getenv('ARTI')
        user=os.getenv('SOEID')
        password=os.getenv('PASSWORD')
        local_home=os.getenv('LOCAL_ARTI')
        artifact_spider=ArtifactsSpider(artifact_url, local_home, user, password)
        artifact_spider.download_artifacts()