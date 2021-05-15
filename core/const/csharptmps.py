#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/18

@author: xcKev
'''

class CSharpConst(object):
    def __init__(self):
        self.KEYS=['class','classBody','namespace']
        self.NAMESPACE='''
using System;
using System.Collections.Generic;
using System.Text;

namespace %s
{
    %s
}
'''
        self.CLASS_OBJ='''
    public class %s
    {
%s
    }
'''
        self.PRIVATE_PROP='''
        public %s %s{set;get;}
        '''