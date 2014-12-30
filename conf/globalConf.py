# -*- encoding: utf-8 -*-
'''
Created on 2014-11-12

@author: huangtx@itg.net
'''
import os

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@172.16.10.170:3306/weixin_py?charset=utf8'
# SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://itgweixindbo:Db0itgweixin@172.16.10.237/itgweixin'

# SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:htx19840809@localhost/weixintest'

SQLALCHEMY_DATABASE_URI_MMS = 'mysql://OATEST:123456789@59.57.246.61:3306/mas?charset=gb2312'

SQLALCHEMY_DATABASE_URI_CMS = 'mssql+pymssql://itggroupcms:itggr0upcns@172.16.10.237/itggroupcmsnew'

SQLALCHEMY_DATABASE_URI_EHR = 'mssql+pymssql://weixin:Nixiew20141229@172.16.10.107/gmhr'

EHR_WSDL_URI = 'http://172.16.10.107/uapws/service/nc.ws.intf.IPsnService?wsdl'

ROOT_PATH = os.path.dirname(__file__)

UPLOAD_FOLDER = '/static/files/'

if __name__ == '__main__':
    pass
