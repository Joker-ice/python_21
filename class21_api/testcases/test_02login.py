"""
========================
@author  :疯疯
@time    :2019/8/29 , 17:27
@E-mail  :1609456360@qq.com
@file    :test_cases.py
@Software: PyCharm
========================
"""
import unittest
from class21_api.mylib.ddt import ddt,data
from class21_api.common.read_excel import ReadExcel
from class21_api.common.myrequests import HttpRequest
from class21_api.common import constant,config
from class21_api.common.logger import log
from class21_api.common.get_data import GetData
import os
#获取错误信息的模块traceback
import traceback
@ddt
class TestCases(unittest.TestCase):
    '''登录接口'''
    conf = config.Config(os.path.join(constant.conf_dir, 'config.ini'))
    get_data = GetData()
    #读取数据表
    readexcel = ReadExcel(os.path.join(constant.data_dir, 'testcases.xlsx'), 'login')
    #获取测试数据
    datas = readexcel.read_excel()
    @data(*datas)
    def test_register(self,data_object):
        log.info('-----------第{}条用例开始执行-------------'.format(data_object.case_id))
        log.info('开始发送请求，请求地址：{}'.format(data_object.url))
        #发送请求
        normal_data = self.get_data.get_replace(data_object.data)
        url = self.conf.get_str('url', 'url') + data_object.url
        get_register = HttpRequest(data_object.method,url,eval(normal_data))
        #获取实际结果，响应内容
        res = get_register.json()
        #获取预期结果
        expected = eval(data_object.expected)
        try:
            #断言实际结果与预期结果是否一致
            self.assertEqual(expected,res)
        except AssertionError as e:
            #结果不同打印未通过
            print('\t该条用例未通过\n\t实际结果与预期结果不一致')
            #调用写入方法，将未通过写入Excel表
            log.info('该条用例未通过：{}'.format(data_object.title))
            # log.error(repr(e)) #获取错误类型函数repr
            # 获取错误信息的方法traceback.format_exc()，str转换成字符串
            log.error(str(traceback.format_exc()))
            self.readexcel.white_excelMax(data_object.case_id+1,'未通过')
            #抛出异常
            raise e
        else:
            #结果相同打印通过
            print('\t该条用例通过\n\t实际结果与预期结果一致')
            # 调用写入方法，将通过写入Excel表
            log.info('该条用例通过：{}'.format(data_object.title))
            self.readexcel.white_excelMax(data_object.case_id + 1, '通过')
        finally:
            print('\t预期结果：{}\n\t实际结果：{}'.format(expected, res))
            # 将实际结果写入Excel表
            self.readexcel.white_excel(data_object.case_id + 1, str(res),8)