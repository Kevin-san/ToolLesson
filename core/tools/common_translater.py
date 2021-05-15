#-*-coding:utf-8-*-
'''
Created on 2021/3/23

@author: xcKev
'''
from PyDictionary import PyDictionary
import goslate
dictionary=PyDictionary()
gs=goslate.Goslate()
def translate2chinese(english_str):
    print(gs.get_languages())
    return dictionary.translate(english_str, "zh")

if __name__ == "__main__":
    print(translate2chinese("hello"))