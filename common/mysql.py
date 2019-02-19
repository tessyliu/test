#-*-coding:utf-8-*-
#@Time    :2019/1/22 16:21
#@Author  :liu_zhenzhen
#@File    :mysql.py
import pymysql  #pip install pymysql
#正常操作步骤：
# #1、新建连接
# host="test.lemonban.com"
# user="test"
# password="test"
# mysql=pymysql.connect(host=host,user=user,password=password,port=3306)
# #2、新建一个查询页面
# cursor=mysql.cursor()
# #3、编写sql语句
# sql="select max(mobilephone) from future.member"
# #4、执行sql
# cursor.execute(sql)
# #5、查看结果
# result=cursor.fetchone()#返回元组
# print(result)
# print(result[0])
# #6、关闭查询
# cursor.close()
# #7、数据库连接关闭
# mysql.close()
from common.read_config import ReadConfig
class MysqlUtil():
    host=ReadConfig().get_value("datebase","host")
    user = ReadConfig().get_value("datebase","user")
    password = ReadConfig().get_value("datebase","password")
    mysql = pymysql.connect(host=host, user=user, password=password, port=3306)
    cursor = mysql.cursor()#在此新建一个查询页面，调用fetch_one函数可进行多次查询

    def fetch_one(self,sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def fetch_all(self,sql):
        self.cursor.execute(sql)
        results=self.cursor.fetchall()
        return

    def close(self):
        self.cursor.close()
        self.mysql.close()

if __name__ == '__main__':
    mysql=MysqlUtil()
    sql = "select max(mobilephone) from future.member"
    result=mysql.fetch_one(sql)
    print(result[0])
    mysql.close()