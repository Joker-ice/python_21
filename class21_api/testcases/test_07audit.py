"""
========================
@author  :疯疯
@time    :2019/9/9 , 16:36
@E-mail  :1609456360@qq.com
@file    :test_07audit.py
@Software: PyCharm
========================
"""
import unittest
from class21_api.mylib.ddt import ddt,data
from class21_api.common import get_data
from class21_api.common.read_excel import ReadExcel
from class21_api.common import constant
from class21_api.common.do_mysql import DoMysql
from class21_api.common.config import Config
from class21_api.common.myrequests import HttpRequest
from class21_api.common.logger import log
#获取错误信息的模块traceback
import traceback
import random
import os
@ddt
class TestCase(unittest.TestCase):
    '''审核接口'''
    conf = Config(os.path.join(constant.conf_dir, 'config.ini'))
    get_data=get_data.GetData()
    #连接数据库
    db = DoMysql()
    #读取Excel表
    read_excel=ReadExcel(os.path.join(constant.data_dir,'testcases.xlsx'),'audit')
    #获取用例数据
    datas = read_excel.read_excel()
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
    @data(*datas)
    def test_audit(self,data_object):
        if '#id#' in data_object.data:
            self.loan()
        #动态参数化请求参数
        data_object.data = self.get_data.get_replace(data_object.data)
        log.info('-----------第{}条用例开始执行-------------'.format(data_object.case_id))
        log.info('开始发送请求，请求地址：{}'.format(data_object.url))
        new_status=None
        #请求参数包含*status*则替换为随机生成的status
        if '*status*' in data_object.data:
            #获取标的当前状态
            status=self.conf.get_str('data','status')
            while True:
                new_status = random.randint(1, 6)
                if new_status != status:#新状态不等于当前状态则替换
                    data_object.data = data_object.data.replace('*status*',str(new_status))
                    break
        #获取完整请求地址
        url = self.conf.get_str('url','url')+data_object.url
        #发送请求
        get_register=HttpRequest(data_object.method,url,eval(data_object.data),get_data.cookies)
        #获取实际结果
        res = get_register.json()['code']
        #获取预期结果
        expected = str(data_object.expected_code)
        # 检验数据库
        res_status = None
        if data_object.check_sql:
            data_object.check_sql = self.get_data.get_replace(data_object.check_sql)
            res_status = self.db.find_one(data_object.check_sql)
        try:
            #断言实际结果和预期结果
            self.assertEqual(expected,res)
            if res_status and new_status:
                self.assertEqual(res_status[0], new_status)
        except AssertionError as e:
            # 结果不同打印未通过
            print('\t该条用例未通过\n\t实际结果与预期结果不一致')
            log.info('该条用例未通过：{}'.format(data_object.title))
            # log.error(repr(e)) #获取错误类型函数repr
            # 获取错误信息的方法traceback.format_exc()，str转换成字符串
            log.error(str(traceback.format_exc()))
            # 调用写入方法，将未通过写入Excel表
            self.read_excel.white_excelMax(data_object.case_id + 1, '未通过')
            # 抛出异常
            raise e
        else:
            #结果相同打印通过
            print('\t该条用例通过\n\t实际结果与预期结果一致')
            # 调用写入方法，将通过写入Excel表
            log.info('该条用例通过：{}'.format(data_object.title))
            self.read_excel.white_excelMax(data_object.case_id + 1, '通过')
        finally:
            print('\t预期结果：{}\n\t实际结果：{}'.format(expected, res))
            # 将实际结果写入Excel表
            self.read_excel.white_excel(data_object.case_id + 1, str(res),8)

    def loan(self):
        id = self.db.find_one('select Id from loan')
        status = self.db.find_one('select Status from loan where Id={}'.format(id[0]))
        self.conf.write_option('data','id',str(id[0]))
        self.conf.write_option('data', 'status', str(status[0]))
r=TestCase()