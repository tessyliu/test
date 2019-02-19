#-*-coding:utf-8-*-
#@Time    :2019/2/15 22:05
#@Author  :liu_zhenzhen
#@File    :test_withdraw.py
import unittest
from common.do_excel import DoExcel
from common import contants
from common.request_method import RequestMethod
from ddt_new import ddt,data
from common.read_config import ReadConfig
import json
from common import context
from common.context import Context
from common import logger
#因充值需要cookies，故单独放在一个类中
#1、充值接口第一条测试用例应该是：正常登录（大前提）
#2、若使用session保持会话的方式进行请求，就需要把request_method的实例化对象放到类里面
#3、获取数据，运行用例

@ddt
class TestWithdraw(unittest.TestCase):
    do_excel=DoExcel(contants.cases_dir)
    cases_withdraw=do_excel.read_excel("withdraw")

    @classmethod
    def setUpClass(cls):#继承unittest.TestCase中的方法，并重写
        print("这是一个类方法")
        cls.request=RequestMethod()#实例化放这里，使用session会话方式
        cls.my_logger = logger.get_logger(logger_name="TestRecharge")


    @data(*cases_withdraw)
    def test_withdraw(self,case):
        self.my_logger.info("开始执行第{}条用例".format(case.case_id))
        data_new=context.replace(case.data)
        resp=self.request.request_method(case.method,case.url,data_new)
        try:
            self.assertEqual(case.expectedresult,resp.json()["code"],"withdraw error")
            # expectedresult在Excel中是code码，这里只判断返回码
            # print(type(case.expectedresult))#在do_excel中已转换expectedresult的数据类型
            # print(type(resp.json()["code"]))

            self.do_excel.write_back(case.case_id+1,resp.text,"Pass")
            self.my_logger.info("取现第{}条用例执行结果：Pass".format(case.case_id))
        except AssertionError as e:
            self.do_excel.write_back(case.case_id+1, resp.text,"Failed")
            self.my_logger.error("取现第{}条用例执行结果：Failed".format(case.case_id))
            raise e

    @classmethod# 此处不要忘了加标识
    def tearDownClass(cls):
        cls.request.close()#类执行完毕，关闭session会话

if __name__=="__main__":
    unittest.main()