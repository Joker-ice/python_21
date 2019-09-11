"""
========================
@author  :疯疯
@time    :2019/8/31 , 17:34
@E-mail  :1609456360@qq.com
@file    :constant.py
@Software: PyCharm
========================
"""
import os
#获取当前项目路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#获取项目下公共方法路径
common_dir = os.path.join(BASE_DIR,'common')
#获取项目下配置文件路径
conf_dir = os.path.join(BASE_DIR,'conf')
#获取项目下测试数据路径
data_dir = os.path.join(BASE_DIR,'data')
#获取项目下日志路径
logs_dir = os.path.join(BASE_DIR,'logs')
#获取项目下测试报告路径
report_dir = os.path.join(BASE_DIR,'report')
#获取项目下测试用例路径
testcases_dir = os.path.join(BASE_DIR,'testcases')