"""
========================
@author  :疯疯
@time    :2019/9/4 , 12:21
@E-mail  :1609456360@qq.com
@file    :test.py
@Software: PyCharm
========================
"""
from class21_api.common.do_mysql import DoMysql
r = DoMysql()
sql = "select Status from loan where Id=23"
res = r.find_one(sql)
print(res)
# count = r.find_count(sql)
#
# print(res)
# from class21_api.common.config import Config
# from class21_api.common import constant
# import os
# conf = Config(os.path.join(constant.conf_dir, 'config.ini'))
# conf.write_option('data','tel','17864116849')
# from class21_api.common.get_data import GetData
# g = GetData()
# cookies=g.get_cookies()
# print(cookies)
# from class21_api.testcases.test_register import TestCases
# a=TestCases()
# a.new_phone()
# 13105485860
# from class21_api.common.myrequests import HttpRequest
# from class21_api.common import get_data
# data={'id':23,'status':4}
# cookies = get_data.cookies
# r = HttpRequest('post','http://test.lemonban.com/futureloan/mvc/api/loan/audit',data,cookies)
# res=r.json()
# print(res)