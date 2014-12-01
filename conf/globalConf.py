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
                db='itgfz2014',
                charset='gbk'
            )

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
