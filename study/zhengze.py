#-*-coding:utf-8-*-
#@Time    :2019/2/14 15:18
#@Author  :liu_zhenzhen
#@File    :zhengze.py
#练习正则
import re
# s='{"mobilephone":"${admin_user}","pwd":"${admin_pwd}"}'
# data={"admin_user":"15873171553","admin_pwd":"123456"}
# p='\$\{(.*?)}'
# m=re.search(p,s)
# print(m)# m:<_sre.SRE_Match object; span=(16, 29), match='${admin_user}'>
# g=m.group()#返回的是整个匹配的字符串
# print(g)
# g1=m.group(1)
# print(g1)
# value=data[g1]
# s=re.sub(p,value,s,count=1)
# print(s)
# l=re.findall(p,s)
# print(l)

def replace(s,d):
    p="\$\{(.*?)}"
    '''
    匹配${}中的内容，即匹配以{开头，以}结束的字符，()只是表示一个组，方便后续调用
    .*匹配单个任意字符并匹配多次，即贪婪匹配，会匹配两次${admin_user}，
    即"${admin_user}","pwd":"${admin_pwd}"，.*？为懒惰匹配，只匹配一次符合条件的字符串
    $为特殊字符需要转义，
    '''
    while re.search(p,s):
        m=re.search(p,s)#任意位置开始查找，找到一个就返回match，一个一个的查找
        key=m.group(1)#取第一个组的匹配字符串，根据序列取，若要取第2组，即group(2)
        value=d[key]#复制
        s=re.sub(p,value,s,count=1)#查找全部，使用正则式查找，并替换，替换全部
    return s

s='{"mobilephone":"${admin_user}","pwd":"${admin_pwd}"}'
data={"admin_user":"15873171553","admin_pwd":"123456"}
s=replace(s,data)
s=eval(s)
print(type(s))