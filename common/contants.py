#-*-coding:utf-8-*-
#@Time    :2019/1/19 23:10
#@Author  :liu_zhenzhen
#@File    :contants.py
import os
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#基本路径
#base_dir=os.path.dirname(os.path.dirname(__file__)) 这样应该也行吧
#print(print(base_dir))

datas_dir=os.path.join(base_dir,"datas")
cases_dir=os.path.join(datas_dir,"cases.xlsx")#cases.xlsx文件路径拼接
#print(cases_dir)

conf_dir=os.path.join(base_dir,"conf")
global_dir=os.path.join(conf_dir,"global.conf")#配置文件路径
test1_dir=os.path.join(conf_dir,"test1.conf")
test2_dir=os.path.join(conf_dir,"test2.conf")

logs_dir=os.path.join(base_dir,"logs")

testcases_dir=os.path.join(base_dir,"testcases")

reports_dir=os.path.join(base_dir,"reports")
report_dir=os.path.join(reports_dir,"report.html")



#步骤
#1、需求分析、用例设计---excel表格（自动化测试用例设计覆盖：功能、逻辑、异常、安全）

#2、数据获取---编写do_excel类（使用类与对象的思想，要灵活）
#坑一：需增加一步：期望结果需要在此统一转换成str类型（因为在断言中做的code的断言，在excel中时
# 无法确保code代码是int还是str类型的）
#坑二：断言的多样性，可断言code、message或断言整个返回结果等

#3、数据获取后解析---编写request类（根据访问的方法get/post。到此步便可实现测试，但日志等并不完整，
# 不便于他人查看测试结果，还需结合单元测试框架）
# 坑一：读取出来的data是str类型，需要转换（该步骤最好在request类中实现）；
# 坑二：eval()的使用场景，eval()是python中的函数，故后面的数据必须是python中的数据格式

#4、结合单元测试unittest和ddt（常量contants的使用）
#坑一：若接口访问方法类似，可在一个类中建立多个函数，每个函数对应一个接口测试
#>>>注册和登录在一个类中，充值在另一个类中（因为充值会用到登录的cookie）
#>>>cookie的两种传递方法：（1）将登录后的resp.cookies，放入到充值的requests.post（）请求中；（2）实例化一个session，
#>>>使用实例化的session去发起request请求（参考request_method类）
#坑二：使用ddt时，循环执行多少次，就有多少条用例，输出的也是真实的用例个数，若使用for i in cases，输出的则是一个用例
#坑三：使用ddt时，若一个测试类中有多个测试方法,在执行用例时（前提一定要添加if __name__），不能单独运行一个测试方法，
# 否则会报错---》原因是：在运行ddt时，会先去找测试类，然后再去找测试方法，若单独运行一个测试方法，会找不到测试类
#坑四：注册用例中有多个地方需要使用新的手机号，那么获取最大手机号的操作，应该放在setup中，而不是setupclass中

#5、优化创造环境数据
#（1）session会话的关闭（self.request.session.close()）
# 设计到类的开始、关闭，将session实例化放入类的开始函数，session会话结束放入类的结束函数
#（2）期望结果只校验code,即Excel中的expected只写返回码(这是需在do_excel中强制转换一下格式)，
# 参考test_recharge类
#（3）优化注册的手机号（方法：在数据库中找到最大的手机号，每次只用用例之前都+1）
##1)学习数据库的连接，并封装成类（参考mysql类）
##a、数据库的连接步骤：建立连接、新建查询页面、编写sql、执行sql、查看结果、关闭查询、关闭连接
##b、执行sql返回的结果是元组类型
##c、数据库连接用完之后一定要记得关闭，占用资源（一般公司的数据库会设置有最大连接数）
# 学习装饰器@unittest.skip("描述内容")：被装饰的方法不执行
#（4）url优化及数据库基础数据配置
# ---》》》配置数据包含：url、基础数据->数据库host、user、password
# ---》》》配置方法：根据不同的测试环境，配置若干套配置数据，并设置一个总开关开控制使用那套环境

#6、用例依赖如何解决----使用正则表达式查找并替换参数化数据：
#（1）正则表达式的一般使用方法：原本字符、元字符、组、.(点)、\d、+、？、*
#（2）正则表达式封装成函数，并应用

#7、编写投资接口测试类及context类
# 场景一：同一个类/module里面，不同测试类之间的数据传递：放到初始化，使用self，，，或者使用全局变量
#场景二：如何解决多个module，或者不同测试类之间的数据传递：利用反射来解决不同测试方法之间的数据传递
#setattr(g1,"hob","swimming")#给实例动态增加属性
# setattr(Girls,"hob","swimming")#给类动态增加属性
# print(getattr(Girls,"hob"))#动态获取类的属性
# print(hasattr(Girls,"male"))#判断是否有male的属性，无则返回Flase
# print(hasattr(Girls,"hob"))#之前动态增加的hob,返回Ture
# 坑：print(hasattr(Girls,"name"))#返回Flase,在初始化函数中的name是实例属性，只有调用实例时才有
#delattr(Girls,"hight")删除类或实例的属性/方法
#坑：Excel中的测试用例data和url一定要写正确，引号一定不能少，注意pwd和password的区别

#8、总结及日志系统重写：
#（1）session的作用：取到前面接口返回的cookie，然后传递到后面接口里面
#（2）request类中使用session通过实例化去进行request请求传递数据，此处存在的误区是：充值、取现、投资等接口服务
# 端需要校验cookies，使用此方法传递数据可行；那么注册、登录等接口传递数据时，服务端不需要校验cookie，那么
#使用此方法也是可行的，因为，服务端不需要校验cookie时却传了cookie，服务端是不判断的，不构成冗余
#（3）ddt的坑：同一类中有多个测试方法时，执行用例时，用例执行顺序可能会乱
# ---》》》解决方法：一个接口对应一个类，一个类包含一个函数
#（4）日志系统重写成函数，配置输出日志的文件路径，实现日志输出级别的可配置
#日志的使用，参考登录接口

#9、run_test加载用例新方法discover、ddt修改源码、Jenkins讲解
#（1）加载用例新方法：discover = unittest.defaultTestLoader.discover((start_dir,pattern='test_*.py',
#                                              top_level_dir=None)
#（2）ddt修改源码：在pip官网下载ddt->修改源代码->重命名ddt_new->可将ddt_放在python的lib目录下，或放在libtex下，使用
# from libtex import ddt_new（HTMLTestRunnerNew同理）
#（3）__dict__的使用：对象.__dict__可以字典形式展示所有实例的属性;类.__dict__可以字典形式获取类属性和方法
#（4）使用git上传代码到jenkens
#（5）Jenkins讲解与使用：基于Java开发的一种持续集成工具，用于监控持续重复的工作
#1）一般公司将源代码放在Git或svn上，然后再从Git或svn上传到jenkins
#2）jenkins端口被占用时，修改端口：jenkins->jenkins.xml中修改
#3)权限弄乱的时候，结果自己无法修改，可进入jenkins->config中删除authorizationStrategy
#4）插件安装：
# 在线插件：svn-安装Subversion Plug-in；git-安装Git;邮箱-安装Email Extension Plugin；管理生成的报表-安装HTML Publisher plugin）
#在线安装失败，去jenkins官网下载.hpi格式文件，浏览选择上传
#5）新建任务：
#General:勾选“丢弃旧的构建”，可设置保存天数
#source code management:配置git或svn拉取代码，或者不配置直接将代码放在workspace下
#Build Triggers:所有选项都不选，默认手动点击“立即构建”触发
#Build Environment：默认不选
#Build：运行方式选择，windows系统选择“执行Windows批命令”，输入“python test_cases\run_test.py”
# (默认是在workspace的项目下执行，所以可以找到run_test.py )
#（若有多个python时，使用D:\Python34\python.exe test_cases\run_test.py全路径）

#


#10、Jenkins定时构造、数据库校验、mock讲解
#（1）Jenkins定时构造：
#（2）数据库校验（以注册为例）：
#（3）mock讲解与应用（以支付系统为例）：
##1）mock应用场景：