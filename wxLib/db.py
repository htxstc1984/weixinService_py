# -*- encoding: utf-8 -*-
'''
Created on 2014-11-11

@author: huangtx@itg.net
'''
import ConfigParser
import threading

from gridfs import GridFS
from pymongo.connection import Connection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from threading import Thread
from jinja2.loaders import PackageLoader
from conf import globalConf
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import create_session, relation
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Text


class nosqlDB:
    initParas = None
    con = None
    db = None
    gfs = None
    instance = None
    locker = threading.RLock()

    @staticmethod
    def _conn():
        if not nosqlDB.con:
            try:
                # config = ConfigParser.ConfigParser()
                # config.readfp(open(PackageLoader('conf','db.ini')))
                nosqlDB.initParas = globalConf.nosqldb
                nosqlDB.con = Connection(host=nosqlDB.initParas['host'], port=nosqlDB.initParas['port'],
                                         max_pool_size=100)
                # nosqlDB.con = MongoClient(host=nosqlDB.initParas['host'], port=nosqlDB.initParas['port'], max_pool_size=200)

                nosqlDB.db = Database(nosqlDB.con, nosqlDB.initParas['db'])
                if nosqlDB.initParas['isauth'] == '1':
                    nosqlDB.db.auth(nosqlDB.initParas['user'], nosqlDB.initParas['passwd'])
                nosqlDB.gfs = GridFS(nosqlDB.db, 'files')
            except BaseException, e:
                print e

    def __init__(self):
        print 'init...'
        self._conn()
        print "server info " + " * "
        print nosqlDB.con.server_info

    @staticmethod
    def getInstance():
        nosqlDB.locker.acquire()
        try:
            if not nosqlDB.instance:
                nosqlDB.instance = nosqlDB()
            return nosqlDB.instance
        except BaseException, e:
            print e
        finally:
            nosqlDB.locker.release()


class mysqlDB:
    engine = None
    locker = threading.RLock()

    @staticmethod
    def create():
        mysqlDB.locker.acquire()
        try:
            mysqlDB.engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' % (
                globalConf.mysqldb['user'], globalConf.mysqldb['passwd'], globalConf.mysqldb['host'],
                globalConf.mysqldb['db']), pool_size=10)
        except BaseException, e:
            raise
        finally:
            mysqlDB.locker.release()

    @staticmethod
    def getSession():
        if mysqlDB.engine == None:
            try:
                mysqlDB.create()
            except BaseException, e:
                raise
        session = create_session(sessionmaker(autocommit=False,
                                              autoflush=False,
                                              bind=mysqlDB.engine))
        return session


if __name__ == '__main__':
    pass
