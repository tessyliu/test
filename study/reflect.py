#-*-coding:utf-8-*-
#@Time    :2019/2/14 13:35
#@Author  :liu_zhenzhen
#@File    :reflect.py
#练习反射
class Girls:
    hight=178
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def sing(self):
        print(self.name+"会唱歌")

g1=Girls("mongo",18)
#setattr(g1,"hob","swimming")#给实例动态增加属性
setattr(Girls,"hob","swimming")#给类动态增加属性
print(g1.hob)#由于编辑器是静态检测语法，故此处会报错，但运行时是正确的

g2=Girls("Lily",30)
print(g2.hob)

print(getattr(Girls,"hob"))#动态获取类的属性
print(hasattr(Girls,"male"))#判断是否有male的属性，无则返回Flase
print(hasattr(Girls,"hob"))#之前动态增加的hob,返回Ture
print(hasattr(Girls,"name"))#返回Flase,在初始化函数中的name是实例属性，只有调用实例时才有
print(hasattr(Girls,"hight"))
# delattr(Girls,"hight")#删除类的属性
# print(getattr(Girls,"hight"))
print(g1.__dict__)
print(Girls.__dict__)


