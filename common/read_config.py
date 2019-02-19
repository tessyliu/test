#-*-coding:utf-8-*-
#@Time    :2019/1/23 14:20
#@Author  :liu_zhenzhen
#@File    :read_config.py
from configparser import ConfigParser
from common import contants
class ReadConfig():
    def __init__(self):#实例化对象时，会自动执行，故放在初始化中
        self.cf=ConfigParser()
        self.cf.read(contants.global_dir,encoding="utf-8")#路径
        open=self.cf.getboolean("switch","open")
        if open:
            self.cf.read(contants.test1_dir)
        else:
            self.cf.read(contants.test2_dir)

    def get_value(self,section,option):
        return self.cf.get(section,option)


if __name__ == '__main__':
    base_url = ReadConfig().get_value("URL", "base_url")
    print(base_url)
    print(type(base_url))