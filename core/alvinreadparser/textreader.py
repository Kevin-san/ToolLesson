# -*- encoding:UTF-8 -*-
'''
Created on 2020/8/8

@author: xcKev
'''
import pyttsx3

class SimpleTextSayer():
    #apt-get install espeak
    def __init__(self,text_str,mp3_file):
        self.text_str=text_str
        self.mp3_file=mp3_file
        self.engine=self.init_engine()
    
    def init_engine(self):
        engine=pyttsx3.init()
        voices=engine.getProperty("voices")
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate',150)
        return engine
    
    def save_to_file(self):
        self.engine.save_to_file(self.text_str,self.mp3_file)
        self.engine.runAndWait()

