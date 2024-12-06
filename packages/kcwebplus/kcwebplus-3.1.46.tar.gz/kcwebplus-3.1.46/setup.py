
# 打包上传 python setup.py sdist upload
# 打包并安装 python setup.py sdist install
############################################# 
from setuptools import setup, find_packages,Extension
import os
def file_get_content(k):
    "获取文件内容"
    if os.path.isfile(k):
        f=open(k,'r',encoding="utf-8")
        con=f.read()
        f.close()
    else:
        con=''
    return con
confkcw={}
confkcw['name']='kcwebplus'                           #项目的名称 
confkcw['version']='3.1.46'							  #项目版本
confkcw['description']='kcwebplus是建立在 kcweb 框架的基础上研发的一套 linux 服务器容器系统'       #项目的简单描述
confkcw['long_description']="其目的是为了解决可视化部署和架构的过程，系统本身是一款服务端管理软件，通过 web 可视化方式管理服务器，提升运维效率"  #项目详细描述
confkcw['license']='Apache License 2.0'                      #开源协议   Apache License 2.0开源
confkcw['url']='https://docs.kwebapp.cn/index/index/3'
confkcw['author']='百里-坤坤'  					 #名字
confkcw['author_email']='kcweb@kwebapp.cn' 	     #邮件地址
confkcw['maintainer']='坤坤' 						 #维护人员的名字
confkcw['maintainer_email']='fk1402936534@qq.com'    #维护人员的邮件地址
def get_file(folder='./',lists=[]):
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if files=='__pycache__' or files=='.git':
                pass
            else:
                lists.append(folder+"/"+files)
                get_file(folder+"/"+files,lists)
        else:
            pass
    return lists
b=get_file("kcwebplus",['kcwebplus'])
setup(
    name = confkcw["name"],
    version = confkcw["version"],
    keywords = "kcwebplus"+confkcw['version'],
    description = confkcw["description"],
    long_description = confkcw["long_description"],
    license = confkcw["license"],
    author = confkcw["author"],
    author_email = confkcw["author_email"],
    maintainer = confkcw["maintainer"],
    maintainer_email = confkcw["maintainer_email"],
    url=confkcw['url'],
    packages =  b,
    install_requires = ['kcweb==6.4.4','pyOpenSSL==23.2.0','chardet==4.0.0','apscheduler==3.6.3','pillow>=10.0.0','oss2>=2.12.1','websocket-client==1.3.1','cryptography==41.0.7'], #第三方包
    package_data = {
        '': ['*.html', '*.js','*.css','*.jpg','*.png','*.gif','server.bat','server.sh','*sqlite/app','*sqlite/index_index'],
    },
    entry_points = {
        'console_scripts':[
            'kcwebplus = kcwebplus.kcwebplus:cill_start'
        ]
    }
)