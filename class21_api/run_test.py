"""
========================
@author  :疯疯
@time    :2019/8/23 , 17:38
@E-mail  :1609456360@qq.com
@file    :class21_day15_test_run.py
@Software: PyCharm
========================
"""
import sys
sys.path.append('./')
import unittest
import os
import time
from HTMLTestRunnerNew import HTMLTestRunner
from class21_api.common import constant
from class21_api.common.logger import log
log.info('---------用例开始执行------------')
#创建测试套件
suite = unittest.TestSuite()
#添加测试用例到套件中
loader = unittest.TestLoader()
#添加一个路径下的所有用例
suite.addTest(loader.discover(constant.testcases_dir))
#打开html文件
#报告名加时间戳
timepath = time.strftime('%Y-%m-%d',time.localtime())
reportfile = '{}-report.html'.format(timepath)
with open(os.path.join(constant.report_dir,reportfile),'wb') as fb:
    #创建运行程序
    runner = HTMLTestRunner(stream=fb,
                            verbosity=2,
                            title='疯疯的测试报告',
                            description='前程贷的测试报告',
                            tester='疯疯')
    runner.run(suite)  #执行运行程序
log.info('---------用例执行结束------------')