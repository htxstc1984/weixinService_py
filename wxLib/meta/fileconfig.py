# -*- encoding: utf-8 -*-
'''
Created on '2014/12/1'

@author: 'hu'
'''
import os
from conf import globalConf

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    globalConf.mysqldb['user'], globalConf.mysqldb['passwd'], globalConf.mysqldb['host'],
    globalConf.mysqldb['db'])
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

if __name__ == '__main__':
    pass