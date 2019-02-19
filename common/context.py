#-*-coding:utf-8-*-
#@Time    :2019/2/13 17:21
#@Author  :liu_zhenzhen
#@File    :context.py
import re

from common.read_config import ReadConfig
config=ReadConfig()

class Context:#上下文类，用例执行前和后的数据的准备和记录
    admin_user = config.get_value("userdata","admin_user")
    admin_pwd = config.get_value("userdata", "admin_pwd")
    loan_member_id =config.get_value("userdata","loan_member_id")
    normal_user=config.get_value("userdata","normal_user")
    normal_pwd = config.get_value("userdata","normal_pwd")
    normal_member_id=config.get_value("userdata","normal_member_id")

def replace(s):#将正则重新修改，不再传入d字典，通过上面的上下文类，去获取数据
    p = "\$\{(.*?)}"
    while re.search(p, s):
        m = re.search(p, s)#任意位置开始查找，找到一个就返回match，一个一个的查找
        key = m.group(1)#取第一个组的匹配字符串:admin_user/admin_pwd/load_id等等，根据序列取，若要取第2组，即group(2)
        if hasattr(Context, key):
            value = getattr(Context, key)#利用反射，动态获取Context的属性
            s = re.sub(p, value, s, count=1)#查找全部，使用正则式查找，并替换，替换全部
        else:
            return None
    return s

if __name__ == '__main__':
    s='{"memberId":"${loan_member_id}","title":"试试人品行不行，借个2W玩玩","amount":20000,"loanRate":"12.0",' \
      '"loanTerm":3,"loanDateType":0,"repaymemtWay":11,"biddingDays":5}'
    # data={"admin_user":"15873171553","admin_pwd":"123456"}
    s=replace(s)
    s=eval(s)
    print(s)
    print(type(s))