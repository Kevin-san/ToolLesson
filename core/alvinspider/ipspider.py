'''
Created on 2021年3月9日

@author: xcKev
'''
from alvinspider import common_spider
from alvintools import common_filer, common_tools
from alvinspider.common_spider import current_log

group_attrs={
    "https://www.kuaidaili.com/free/inha/%s/":{"index_tag":"table","index_attrs":{"class":"table table-bordered table-striped"},"content_tag":"tr","ip_index":1,"port_index":2},
    "https://www.89ip.cn/index_%s.html":{"index_tag":"table","index_attrs":{"class":"layui-table"},"content_tag":"tr","ip_index":1,"port_index":2},
    "http://m.66ip.cn/%s.html":{"index_tag":"div","index_attrs":{"class":"containerbox boxindex"},"content_tag":"tr","ip_index":1,"port_index":2},
}

class IpSpider():
    def __init__(self, url, map_attrs):
        url_items = url.split('/')
        self.home_url = '/'.join(url_items[0:3])
        self.ip_url = url
        self.index_attrs = map_attrs["index_attrs"]
        self.index_tag = map_attrs["index_tag"]
        self.content_tag = map_attrs["content_tag"]
        self.ip_id=map_attrs["ip_index"]
        self.port_id=map_attrs["port_index"]
        self.name = "valid_ip_list.txt"
        self.ip_list=[]
        if common_filer.exists(self.name):
            ip_handler=open(self.name,"r",encoding="utf8")
            self.ip_list=ip_handler.readlines()
            ip_handler.close()
        self.ip_w=open(self.name,"w+",encoding="utf8")

    def get_html_text(self,index_no):
        return common_spider.get_response_text(self.ip_url % index_no, "", "",3, self.home_url)
    
    def get_ip_list(self,end_cnt):
        valid_ip_list=[]
        for i in range(1,end_cnt):
            html_txt=self.get_html_text(i)
            table_area=common_spider.get_beautifulsoup_from_html(html_txt, self.index_tag, self.index_attrs)
            table_body=table_area[0].find("tbody")
            table_trs=table_body.find_all(self.content_tag)
            for table_tr in table_trs:
                table_td = common_spider.get_beautifulsoup_from_html(str(table_tr), "td", {})
                ip_port=table_td[self.ip_id-1].text.replace("\n","").strip()+":"+table_td[self.port_id-1].text.replace("\n","").strip()
                if common_spider.check_valid_ip(ip_port):
                    valid_ip_list.append(ip_port)
                    self.ip_w.write(F"{ip_port}\n")
        for ip in self.ip_list:
            ip_port=ip.replace("\n","")
            if common_spider.check_valid_ip(ip_port) and ip_port not in valid_ip_list:
                valid_ip_list.append(ip_port)
                self.ip_w.write(F"{ip_port}\n")
        self.ip_w.close()
        return valid_ip_list

if __name__ == '__main__':
    end_cnt=50
    for key, vals in group_attrs.items():
        ipspider=IpSpider(key,vals)
        ipspider.get_ip_list(end_cnt)