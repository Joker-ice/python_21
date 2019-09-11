"""
========================
@author  :疯疯
@time    :2019/9/4 , 11:32
@E-mail  :1609456360@qq.com
@file    :do_mysql.py
@Software: PyCharm
========================
"""
from class21_api.common import constant
from class21_api.common.config import Config
import pymysql
import os

class DoMysql():
    '''操作mysql数据库类'''
    conf = Config(os.path.join(constant.conf_dir, 'config.ini'))
    db_config = conf.get_other('mysql','db_config')#从配置文件读取连接数据库的参数字典
    def __init__(self):
        #创建连接
        self.conn = pymysql.connect(**self.db_config)
        #创建游标
        self.cur=self.conn.cursor()
    def close(self):
        '''关闭连接'''
        #关闭游标
        self.cur.close()
        #断开连接
        self.conn.close()
    def find_one(self,sql):
        '''获取单条数据'''
        self.cur.execute(sql)
        res=self.cur.fetchone()
        self.conn.commit()
        return res
    def find_all(self,sql):
        '''获取全部数据'''
        self.cur.execute(sql)
        res=self.cur.fetchall()
        self.conn.commit()
        return res
    def find_count(self,sql):
        '''获取受影响条数'''
        count=self.cur.execute(sql)
        self.conn.commit()
        return count