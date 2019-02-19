#-*-coding:utf-8-*-
#@Time    :2019/1/19 23:10
#@Author  :liu_zhenzhen
#@File    :request_method.py.py
import requests
import json
from common.read_config import ReadConfig
class RequestMethod:
    def __init__(self):
        self.session=requests.sessions.Session()    #实例化一个session，老的写法requests.session()已经淘汰


    def request_method(self,method,url,data=None):
        base_url = ReadConfig().get_value("URL", "base_url")
        total_url=base_url+url#url拼接

        method=method.upper()   #将字符统一转换成大写
        if data is not None and type(data)==str:
            data = eval(data) #将字符串转换为dict格式/或者用json.loads()
        print("method：{}".format(method))#将方法、url、data等在运行结果中展示出来
        print("url：{}".format(total_url))
        print("data：{}".format(data))
        print(type(data))

        if method=="GET":
            resp=self.session.request(method, url=total_url, params=data)
            print("response：{}".format(resp.text))
            return resp

        elif method=="POST":
            resp = self.session.request(method,url=total_url,data=data)
            print("response：{}".format(resp.text))
            return resp
        else:
            print("Un-support method!!!")

    def close(self):
        self.session.close()#关闭session
