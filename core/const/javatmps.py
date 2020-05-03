#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/1

@author: xcKev
'''

class JavaConst(object):
    def __init__(self):
        self.GETTER='''
        public %s get%s(){
            return this.%s;
        }'''
        self.SETTER='''
        public void set%s(%s %s){
            this.%s=%s;
        }'''
        self.PRI_PROP="private %s %s;"
        self.METHOD='''
        public %s %s(%s) %s 
        {
            %s
        }'''
        self.ABSTRACT_METHOD="public abstract %s %s(%s) %s;"
        self.STATIC_METHOD='''
        public static %s %s(%s) %s {
            %s
        }'''
        self.PRI_CONSTRUCTOR="private %s(){}"
        self.CONSTRUCTOR='''
        public %s(%s){
            %s
        }'''
        self.PACKAGE="package %s;"
        self.CLASS_OBJ='''
        public class %s{
            %s
        }'''
        self.INTERFACE_OBJ='''
        public interface %s{
            %s
        }'''
        self.IMPORTS="import %s;"
        self.THIS_VAL="this.%s=%s;"
        self.DEF_LIST="List<%s> %s = new ArrayList<>();"
        self.SET_LIST="%s.add(%s);"
        self.SET_STR_LIST='%s.add("%s");'
        self.DEF_MAP="Map<%s,%s> %s = new HashMap<>();"
        self.SET_MAP="%s.put(%s,%s);"
        self.SET_STR_KEY_MAP='%s.put("%s",%s);'
        self.SET_STR_VAL_MAP='%s.put(%s,"%s");'
        self.SET_STR_ALL_MAP='%s.put("%s","%s");'
        self.CONSTANT='public static final String %s="%s";'
        self.MAIN_METHOD="public static void main(String[] args){%s}"
        self.PARAMETER="%s %s"    
