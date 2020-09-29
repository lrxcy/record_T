# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pymysql #导入mysql的连接模块


mpl.rcParams['font.sans-serif']=['KaiTi']
mpl.rcParams['font.serif']=['KaiTi']    # 导入需要用到的常用库
conn=pymysql.connect(user='xxx',password='xxx',database='xxx')    # 设置连接用户名密码数据库等
cursor=conn.cursor()    # 设置游标 设置了才能正常查询

def mysql(sql):
   cursor.execute(sql)    # 执行查询语句
   jieguo=cursor.fetchall()   # 查看全部查询结果
   cols=cursor.description    # 类似 desc table_name返回结果
   col=[]     # 创建一个空列表以存放列名
   for v in cols:
      col.append(v[0])     # 循环提取列名，并添加到col空列表
   pd.set_option('display.max_rows', 500)     # 显示的最大行数
   pd.set_option('display.max_columns', 500)      # 显示的最大列数
   pd.set_option('display.width', 1000)       # 横向最多显示多少个字符
   pd.set_option('max_colwidth', 5000)        # 列长度
   pd.set_option('colheader_justify', 'right')     # 显示居中还是左边
   pd.set_option('expand_frame_repr', False)      # True就是可以换行显示。设置成False的时候不允许换行
   df_sql=pd.DataFrame(jieguo, columns=col)   # 将查询结果转换成DF结构，并给列重新赋值
   if df_sql.empty:
      return 'empty set'  # 判断查询结果为空时返回的值
   else:
      return df_sql   # 以DF结构返回查询结构，DF.to_excel...导出查询结果时可以带列名，这样就解决了mysql直接导出结果无列名的问题


if __name__ == "__main__":
   sql = "show tables;"
   print(mysql(sql))
