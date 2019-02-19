#-*-coding:utf-8-*-
#@Time    :2019/2/18 12:37
#@Author  :liu_zhenzhen
#@File    :logger.py
import logging
from logging.handlers import RotatingFileHandler
from common import contants
import os

def get_logger(logger_name):
    my_logger = logging.getLogger(logger_name)#logger_name是模块名，登录、投资等
    my_logger.setLevel("DEBUG")#一般设置最低的
    formatter = logging.Formatter("[%(asctime)s]-[%(levelname)s]-[%(name)s]-[日志信息:%(message)s]-[%(lineno)d]")

    file_name = os.path.join(contants.logs_dir,"case.log")#设置日志文件路径，在logs文件夹下,使用绝对路径
    file_handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=20*1024*1024, backupCount=10, encoding="utf-8")
    #maxBytes是最大字节数，backupCount是备份次数
    file_handler.setLevel("INFO")#文件输出级别和控制输出级别可在配置文件中配置，此处未配置，感觉配置后不方便查看，不直观
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel("DEBUG")#输出到控制台，定义输出级别
    console_handler.setFormatter(formatter)

    my_logger.addHandler(file_handler)
    my_logger.addHandler(console_handler)#此处不用移除渠道

    return my_logger