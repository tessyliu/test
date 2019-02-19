#-*-coding:utf-8-*-
#@Time    :2019/2/18 16:42
#@Author  :liu_zhenzhen
#@File    :run_test.py
import unittest
from common import contants
import HTMLTestRunnerNew

discover = unittest.defaultTestLoader.discover(contants.testcases_dir,pattern='test_*.py',
                                               top_level_dir=None)
with open(contants.report_dir,"wb+") as file:
    runner=HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                            title="接口测试报告title",
                                            description="接口测试报告description",
                                            tester="Liu")
    runner.run(discover)