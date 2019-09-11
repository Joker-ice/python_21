"""
========================
@author  :疯疯
@time    :2019/8/30 , 14:58
@E-mail  :1609456360@qq.com
@file    :myrequests_cookies.py
@Software: PyCharm
========================
"""
import requests
from requests import session
class HttpSession(object):
    '''保存cookies信息的请求类'''
    s = session()  # 创建session对象
    def __init__(self,mothed,url,data,headers=None):
        '''
        初始化数据
        :param mothed: 请求方式
        :param url: 请求地址
        :param data: 请求参数
        :param headers: 请求头
        '''
        self.mothed = mothed
        self.url = url
        self.data = data
        self.headers = headers

    def request(self):
        '''发送请求'''
        if self.mothed.lower() == 'get':#如果传入的请求方式为get，则调用get方法发送请求
            try:
                res = self.s.get(url=self.url, params=self.data,headers=self.headers)
            except Exception as e:
                print('get请求发送错误{}'.format(e))
            else:
                return res.cookies  #返回cookies
        elif self.mothed.lower() == 'post':#如果传入的请求方式为post，则调用post方法发送请求
            try:
                res = self.s.post(url=self.url, data=self.data,headers=self.headers)
            except Exception as e:
                print('post请求发送错误{}'.format(e))
            else:
                return res.cookies #返回cookies
        else:
            print('您的请求方式为{},不是get/post,请核对'.format(self.mothed))  # 不是get/post给出用户提示

class HttpRequest(object):
    '''不保存cookies信息的请求类'''
    def __init__(self, method, url, data,cookies=None,headers=None):
        '''
        初始化数据
        :param method: 请求方式
        :param url: 请求地址
        :param data: 请求参数
        :param cookies: cookies
        :param headers: 请求头
        '''
        self.method = method
        self.url = url
        self.data = data
        self.cookies = cookies
        self.headers = headers

    def request(self):
        '''发送请求'''
        if self.method.lower() == 'get':#如果传入的请求方式为get，则调用get方法发送请求
            try:
                self.res = requests.get(url=self.url, params=self.data,cookies=self.cookies,headers=self.headers)
            except Exception as e:
                print('get请求发送错误{}'.format(e))
        elif self.method.lower() == 'post':#如果传入的请求方式为post，则调用post方法发送请求
            try:
                self.res = requests.post(url=self.url, data=self.data,cookies=self.cookies,headers=self.headers)
            except Exception as e:
                print('get请求发送错误{}'.format(e))
        else:
            print('您的请求方式为{},不是get/post,请核对'.format(self.method))  # 不是get/post给出用户提示

    def text(self):
        '''获取text格式的响应信息'''
        self.request()#发送请求
        return self.res.text#返回响应信息

    def json(self):
        '''获取json格式的响应信息'''
        self.request()#发送请求
        return self.res.json()#返回响应信息

    def content(self):
        '''获取content格式的响应信息'''
        self.request()#发送请求
        return self.res.content.decode('utf8')#返回响应信息

if __name__ == '__main__':
    data = {'mobilephone':'17864116846',
            'pwd':'123456',
            'regname':'疯疯'}
    data1 = {'mobilephone':'17864116846',
            'amount':123}
    r = HttpSession('get','http://test.lemonban.com/futureloan/mvc/api/member/login',data)
    r1 = HttpRequest('post','http://test.lemonban.com/futureloan/mvc/api/member/recharge',data1,r)
    print(r1.content())