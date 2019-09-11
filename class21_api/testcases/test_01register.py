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
from class21_api.common import constant
from class21_api.common.logger import log
from class21_api.common.do_mysql import DoMysql
from class21_api.common.get_data import GetData
from class21_api.common.config import Config
import random
import os
#获取错误信息的模块traceback
import traceback
@ddt
class TestCases(unittest.TestCase):
    '''注册接口'''
    conf = Config(os.path.join(constant.conf_dir, 'config.ini'))
    get_data = GetData()
    #打开数据库
    db=DoMysql()
    #读取数据表
    readexcel = ReadExcel(os.path.join(constant.data_dir, 'testcases.xlsx'), 'register')
    #获取测试数据
    datas = readexcel.read_excel()
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
    @data(*datas)
    def test_register(self,data_object):
        log.info('-----------第{}条用例开始执行-------------'.format(data_object.case_id))
        log.info('开始发送请求，请求地址：{}'.format(data_object.url))
        #随机生成注册用手机号
        phone = None
        if '*tel*' in data_object.data:
            phone = self.new_phone()
            data_object.data=data_object.data.replace('*tel*',phone)
        #发送请求
        normal_data = self.get_data.get_replace(data_object.data)
        url = self.conf.get_str('url', 'url') + data_object.url
        get_register = HttpRequest(data_object.method,url,eval(normal_data))
        #获取实际结果，响应内容
        res = get_register.json()
        #获取预期结果
        expected = data_object.expected
        # 注册后数据库数据条数
        sql_res = None
        if data_object.check_sql: #若用例数据sql字段不为空则执行
            normal_sql = data_object.check_sql.replace('*tel*',phone)
            sql_res=self.db.find_count(normal_sql) #获取受影响行数
        try:
            #断言实际结果与预期结果是否一致
            self.assertEqual(eval(expected),res)
            if sql_res: #若受影响行数不为空执行
                self.assertEqual(1,sql_res) #断言用例执行前和执行后受影响行数
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
    def new_phone(self):
        '''随机生成手机号'''
        while True:
            phone = '131'
            for i in range(8):
               i = random.randint(0,9)
               phone+=str(i)
            #到数据库比对
            sql = "select * from member where MobilePhone='{}'".format(phone)
            #数据库中不存在，则返回生成的手机号
            if self.db.find_count(sql)==0:
                return phone