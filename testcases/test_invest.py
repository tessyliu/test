#-*-coding:utf-8-*-
#@Time    :2019/2/14 15:43
#@Author  :liu_zhenzhen
#@File    :test_invest.py
import unittest
import json
from common.do_excel import DoExcel
from common import contants
from common.request_method import RequestMethod
from ddt_new import ddt,data
from common.read_config import ReadConfig
from common import context
from common.context import Context
from common.mysql import MysqlUtil
from common import logger

@ddt
class TestInvest(unittest.TestCase):
    do_excel=DoExcel(contants.cases_dir)
    cases_invest=do_excel.read_excel("invest1")

    @classmethod
    def setUpClass(cls):#继承unittest.TestCase中的方法，并重写
        print("这是一个类方法")
        cls.request=RequestMethod()#实例化放这里，使用session会话方式
        cls.mysql=MysqlUtil()#实例化就开始建立连接
        cls.my_logger = logger.get_logger(logger_name="TestRecharge")

    def setUp(self):  # 每个测试方法里面去运行的操作放到类方法里面
        print("这是一个setUP")
        pass

    @data(*cases_invest)
    def test_invest(self,case):
        self.my_logger.info("开始执行第{}条用例".format(case.case_id))
        data_new = context.replace(case.data)#替换数据
        print(data_new)
        print(type(data_new))
        resp = self.request.request_method(case.method, case.url, data_new)
        try:
            self.assertEqual(case.expectedresult,resp.json()["code"],"invest error")
            self.do_excel.write_back(case.case_id+1,resp.text,"Pass")
            self.my_logger.info("投资第{}条用例执行结果：Pass".format(case.case_id))
            if resp.json()["msg"]=="加标成功":#在加标用例执行成功后，根据msg判断是否加标成功，进而执行下一条审核标的用例时，使用loan_id
                loan_member_id=getattr(Context,"loan_member_id")#加标成功后，获取loan_member_id
                sql="select id from future.loan where memberID='{0}'" \
                    "order by createTime desc limit 1".format(loan_member_id)#根据loan_member_id查找到loan_id
                loan_id=self.mysql.fetch_one(sql)[0]#loan_id为int,动态给Context增加loan_id属性
                print(loan_id)
                print(type(loan_id))
                setattr(Context, "loan_id", str(loan_id))#loan_id应与excel中设置一致

        except AssertionError as e:
            self.do_excel.write_back(case.case_id+1, resp.text,"Failed")
            self.my_logger.error("投资第{}条用例执行结果：Failed".format(case.case_id))
            raise e

    @classmethod# 此处不要忘了加标识
    def tearDownClass(cls):
        cls.request.close()#类执行完毕，关闭session会话
        cls.mysql.close()#关闭数据库

if __name__=="__main__":
    unittest.main()