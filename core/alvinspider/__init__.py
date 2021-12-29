class SpiderAttribute():
    
    def __init__(self,tag_name,id_v="",class_v="",index=1,output_href="a.href",output_text="a.text"):
        self.tag=tag_name
        self.id=id_v
        self.class_vals=class_v
        self.index=index
        self.output_href=output_href
        self.output_text=output_text
        self.dict_attrs=self.to_attrs()
    
    def to_attrs(self):
        dict_attrs=dict()
        if self.id:
            dict_attrs["id"]=self.id
        if self.class_vals:
            dict_attrs["class"]=self.class_vals
        return dict_attrs

class SpiderParameters():
    def __init__(self,home_path,key_category,key,val,url_attrs):
        self.home_path=home_path
        self.key_category=key_category
        self.key=key
        self.val=val
        self.url_attrs=url_attrs
    
class GroupAttribute():
    
    def get_dict(self,attribute):
        attrs=dict()
        if attribute.id:
            attrs["id"]=attribute.id
        if attribute.class_vals:
            attrs["class"]=attribute.class_vals
        return attrs
    
    def __init__(self,block_attribute,item_attribute,children_attribute,page_attribute):
        self.block_tag=block_attribute.tag
        self.block_attrs=self.get_dict(block_attribute)
        self.item_tag=item_attribute.tag
        self.item_attrs=self.get_dict(item_attribute)
        self.children_tag=children_attribute.tag
        self.children_index=children_attribute.index
        self.children_href=children_attribute.output_href
        self.children_text=children_attribute.output_text
        self.page_tag=page_attribute.tag
        self.page_attrs=self.get_dict(page_attribute)
    
    @staticmethod
    def get_block_spider_attribute(attr_dict):
        return SpiderAttribute(tag_name=attr_dict["block_tag"],id_v=attr_dict["block_id"],class_v=attr_dict["block_class"])
    
    @staticmethod
    def get_item_spider_attribute(attr_dict):
        return SpiderAttribute(tag_name=attr_dict["item_tag"],id_v=attr_dict["item_id"],class_v=attr_dict["item_class"])
    
    @staticmethod
    def get_children_spider_attribute(attr_dict):
        return SpiderAttribute(tag_name=attr_dict["children_tag"],index=attr_dict["children_index"],output_href=attr_dict["children_href"],output_text=attr_dict["children_text"])
    
    @staticmethod
    def get_page_spider_attribute(attr_dict):
        return SpiderAttribute(tag_name=attr_dict["page_tag"],id_v=attr_dict["page_id"],class_v=attr_dict["page_class"])


class SpiderIndexItem():
    def __init__(self,index_url,content_list):
        self.index_url=index_url
        self.content_list=content_list
        
class SpiderContentItem():
    def __init__(self,a_href,a_text,spider_val):
        self.a_href=a_href
        self.a_text=a_text
        self.spider_val=spider_val

class SpiderImgItem():
    def __init__(self,url,img_src,file_path):
        self.url=url
        self.img_src=img_src
        self.file_path=file_path

class SpiderNovelItem():
    def __init__(self,title_name,url,novel_detail,file_path):
        self.title_name=title_name
        self.url=url
        self.novel_detail=novel_detail
        self.file_path=file_path

class SpiderVideoItem():
    def __init__(self,url,episode_name,file_path):
        self.url=url
        self.episode_name=episode_name
        self.file_path=file_path
    