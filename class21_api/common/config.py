"""
========================
@author  :疯疯
@time    :2019/8/29 , 1:51
@E-mail  :1609456360@qq.com
@file    :config.py
@Software: PyCharm
========================
"""
from configparser import ConfigParser
from class21_api.common import constant
import os
class Config(ConfigParser):
    '''配置文件类'''
    def __init__(self,configname):
        '''读取配置文件'''
        self.conf = ConfigParser()
        self.conf.read(configname,encoding='utf8')

    def get_str(self,section,option):
        '''查询option（字符串类型）'''
        return self.conf.get(section,option) #返回获取到的内容

    def get_int(self,section,option):
        '''查询option（整数类型）'''
        return self.conf.getint(section,option) #返回获取到的内容

    def get_float(self,section,option):
        '''查询option（浮点数类型）'''
        return self.conf.getfloat(section,option) #返回获取到的内容

    def get_boolean(self,section,option):
        '''查询option（布尔类型）'''
        return self.conf.getboolean(section,option) #返回获取到的内容

    def get_other(self,section,option):
        '''查询option（其他类型）'''
        return eval(self.conf.get(section,option)) #返回获取到的内容

    def write_section(self,section):
        '''写入section配置块'''
        self.conf.add_section(section)
        self.conf.write(open(os.path.join(constant.conf_dir,'config.ini'),'w',encoding='utf8'))

    def write_option(self,section,option,value):
        '''写入option配置项'''
        self.conf.set(section,option,value)
        self.conf.write(open(os.path.join(constant.conf_dir,'config.ini'),'w',encoding='utf8'))