# -*- encoding: utf-8 -*-
'''
Created on 2014-11-12

@author: huangtx@itg.net
'''

mysqldb = dict(
                driverName='mysql',
                host='172.16.10.170' ,
                port=3306,
                user='root',
                passwd='root',
                db='weixin_py',
                charset='utf8'
            )

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@172.16.10.170:3306/weixin_py?charset=utf8'
EHR_WSDL_URI = 'http://172.16.10.107/uapws/service/nc.ws.intf.IPsnService?wsdl'

nosqldb = dict(
                driverName='mongo',
                host='172.16.10.170' ,
                port=27017,
                user='admin',
                passwd='admin',
                db='blog',
                isauth = 0
            )
if __name__ == '__main__':
    pass
