#-*- encoding:UTF-8 -*-
'''
Created on 2019/6/1

@author: xcKev
'''

class _const():
    def __init__(self):
        self.sql_column_types=["varchar","varchar2","date","datetime","bigint","smallint","tinyint","text","int","number","decimal","double","numeric","char"]
        self.sql_java_col_map={"varchar":"String","date":"java.sql.Date","datetime":"java.sql.Timestamp","bigint":"BigInteger","smallint":"Integer","tinyint":"Integer","text":"Text","int":"Integer","number":"java.math.BigDecimal","decimal":"java.math.BigDecimal","double":"java.math.BigDecimal","numeric":"java.math.BigDecimal","char":"String"}
        self.sql_csharp_col_map={"varchar":"string","date":"Date","datetime":"DateTime","bigint":"int","smallint":"int","tinyint":"int","text":"string","int":"int","number":"decimal","decimal":"decimal","double":"decimal","numeric":"decimal","char":"string"}