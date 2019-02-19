#-*-coding:utf-8-*-
#@Time    :2019/1/18 13:24
#@Author  :liu_zhenzhen
#@File    :test_api.py
import unittest
from common.do_excel import DoExcel
from common import contants
from common.request_method import RequestMethod
from common.mysql import MysqlUtil
import json
from common.read_config import ReadConfig
from common import logger
import ddt_new
from ddt_new import ddt,data

@ddt
class TestApi(unittest.TestCase):
    do_excel = DoExcel(contants.cases_dir )#do_excel
    cases_login = do_excel.read_excel('login')
    cases_register = do_excel.read_excel('register')
    request_1 = RequestMethod()#request
    mysql = MysqlUtil()#数据库
    my_logger = logger.get_logger(logger_name = "TestApi")#各个模块中的logger_name可设置成一个名字

    def setUp(self):
        pass

    #@unittest.skip("不要运行")#被装饰的方法将不会被执行
    @data(*cases_login)#登录接口测试
    def test_login(self,case):
        self.my_logger.info("开始执行第{}条登录用例".format(case.case_id))
        resp = self.request_1.request_method(case.method,case.url,case.data)
        try:
            self.assertEqual(case.expectedresult, resp.text)
            self.do_excel.write_back(case.case_id + 1, resp.text, "Pass")
            #问题一：为啥登录的实际结果可以写进Excel，执行结果pass/failed却写不进Excel呢？？？？？？？？？
            self.my_logger.info("第{}条登录用例执行结果：Pass".format(case.case_id))
        except AssertionError as e:
            self.do_excel.write_back(case.case_id + 1, resp.text, "Failed")
            self.my_logger.error("第{}条登录用例执行结果：Failed".format(case.case_id))
            raise e

    def tearDown(self):
        pass

    @unittest.skip("不执行注册用例")
    @data(*cases_register)#注册接口测试
    def test_register(self, case):
        self.my_logger.info("开始执行第{}条注册用例".format(case.case_id))
        sql = "select max(mobilephone) from future.member"
        max = self.mysql.fetch_one(sql)[0]  # 返回结果是元组类型数据，放在此处，执行每一条用例时都会替换新的手机号
        data_dict=json.loads(case.data)#case.data从Excel取出是字符串格式，需转换为字典
        if data_dict["mobilephone"]=="${register_mobile}":#手机号参数化
            data_dict["mobilephone"]=int(max)+1
            print(data_dict["mobilephone"])
        resp = self.request_1.request_method(case.method,case.url,data_dict)
        try:
            self.assertEqual(case.expectedresult,resp.text)
            self.do_excel.write_back(case.case_id + 1, resp.text, "Pass")
            self.my_logger.info("第{}条注册用例执行结果：Pass".format(case.case_id))
        except AssertionError as e:
            self.do_excel.write_back(case.case_id + 1, resp.text, "Failed")
            self.my_logger.error("第{}条注册用例执行结果：Failed".format(case.case_id))
            raise e

if __name__=="__main__":
    unittest.main()