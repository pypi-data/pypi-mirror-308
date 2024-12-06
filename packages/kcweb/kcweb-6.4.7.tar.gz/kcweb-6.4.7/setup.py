
# 打包上传 python setup.py sdist upload
# 打包并安装 python setup.py sdist install
# twine upload --repository-url https://test.pypi.org/legacy/ dist/* #上传到测试
# pip install --index-url https://pypi.org/simple/ kcweb   #安装测试服务上的kcweb pip3 install kcweb==4.12.4 -i https://pypi.org/simple/
# 安装 python setup.py install
############################################# 
import os,sys
from setuptools import setup, find_packages,Extension
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, current_dir)
from kcweb import config
confkcw={}
confkcw['name']=config.kcweb['name']                             #项目的名称 
confkcw['version']=config.kcweb['version']							#项目版本
confkcw['description']='kcweb作为web开发而设计的高性能框架，采用全新的架构思想，注重易用性。遵循MIT开源许可协议发布，意味着个人和企业可以免费使用kcweb，甚至允许把你基于kcweb开发的应用开源或商业产品发布或销售。完整文档请访问：https://intapp.kwebapp.cn/intapp/doc/index/finddoc/1'       #项目的简单描述
confkcw['long_description']=config.kcweb['long_description']     #项目详细描述
confkcw['license']=config.kcweb['license']                    #开源协议   mit开源
confkcw['url']=config.kcweb['url']
confkcw['author']=config.kcweb['author']  					 #名字
confkcw['author_email']=config.kcweb['author_email'] 	     #邮件地址
confkcw['maintainer']=config.kcweb['maintainer'] 						 #维护人员的名字
confkcw['maintainer_email']=config.kcweb['maintainer_email']    #维护人员的邮件地址
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
b=get_file("kcweb",['kcweb'])
setup(
    name = confkcw["name"],
    version = confkcw["version"],
    keywords = "kcweb"+confkcw['version'],
    description = confkcw["description"],
    long_description = confkcw["long_description"],
    license = confkcw["license"],
    author = confkcw["author"],
    author_email = confkcw["author_email"],
    maintainer = confkcw["maintainer"],
    maintainer_email = confkcw["maintainer_email"],
    url=confkcw['url'],
    packages =  b,
    install_requires = ['kcw==2.6.4','PyMySQL==0.9.3','redis==3.3.8','python-dateutil==2.9.0','pymongo==3.10.0','Mako==1.3.6','six>=1.12.0','websockets==8.1'], #第三方包
    package_data = {
        '': ['*.html', '*.js','*.css','*.jpg','*.png','*.gif'],
    },
    entry_points = {
        'console_scripts':[
            'kcweb = kcweb.kcweb:cill_start'
        ]
    }
)