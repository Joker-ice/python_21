"""
========================
@author  :疯疯
@time    :2019/8/25 , 15:42
@E-mail  :1609456360@qq.com
@file    :logger.py
@Software: PyCharm
========================
"""
import os
import time
import logging
from class21_api.common.config import Config
from class21_api.common import constant
import os

class Logger(object):
    #日志封装类
    conf = Config(os.path.join(constant.conf_dir, 'config.ini'))
    logger_level = conf.get_str('log', 'logger_level')
    s_level = conf.get_str('log', 's_level')
    f_level = conf.get_str('log', 'f_level')
    def __new__(cls, *args, **kwargs):
        logger = logging.getLogger()
        # 修改log的保存位置
        times = time.strftime('%Y-%m-%d', time.localtime())  # 获取系统时间
        logfilename = '%s.log' % times  # 用时间给日志文件命名
        logpathname = os.path.join(constant.logs_dir,logfilename)
        # 创建输出渠道到文件
        rotatingFileHandler = logging.FileHandler(filename=logpathname, mode='a', encoding='utf8')
        # 用Formatter格式化函数设置输出格式
        formatter = logging.Formatter('[%(asctime)s] - [%(filename)s-->line:%(lineno)d] - [%(levelname)s] : %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置文件输出格式
        rotatingFileHandler.setFormatter(formatter)
        # 设置文件输出等级
        rotatingFileHandler.setLevel(cls.f_level)
        # 控制台输出
        console = logging.StreamHandler()
        # 设置控制台输出等级
        console.setLevel(cls.s_level)
        # 设置控制台输出格式
        console.setFormatter(formatter)
        # 添加输出渠道到日志收集器
        logger.addHandler(rotatingFileHandler)
        logger.addHandler(console)
        # 设置日志收集等级
        logger.setLevel(cls.logger_level)
        return logger
log = Logger()