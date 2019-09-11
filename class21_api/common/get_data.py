"""
========================
@author  :疯疯
@time    :2019/9/5 , 18:37
@E-mail  :1609456360@qq.com
@file    :get_data.py
@Software: PyCharm
========================
"""
from class21_api.common.myrequests import HttpSession
from class21_api.common.config import Config
from class21_api.common import constant
import os
import re
# 读取配合文件
conf = Config(os.path.join(constant.conf_dir, 'config.ini'))
# 获取登录地址
login_url = conf.get_str('login_cookie', 'login_url')
# 获取登录参数
login_data = eval(conf.get_str('login_cookie', 'data'))
# 发送请求获取cookies
response = HttpSession('post', login_url, login_data)
cookies = response.request()
class GetData(object):
    def get_replace(self,target):
        '''
        参数化用例数据
        :param target:用例请求参数
        :return:
        '''
        config=Config(os.path.join(constant.conf_dir, 'config.ini'))
        params='#(.*?)#' #正则匹配规则
        while re.search(params,target):
            match = re.search(params,target) #拿到匹配到的字符串
            key = match.group(1)  #获取内容作为key
            value = config.get_str('data',key)  #通过key到配置文件中获取值
            target=re.sub(params,value,target,count=1)  #用获取到值替换匹配的字符串
        return target
