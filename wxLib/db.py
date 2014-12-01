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
#                 config = ConfigParser.ConfigParser()
#                 config.readfp(open(PackageLoader('conf','db.ini')))
                nosqlDB.initParas = globalConf.nosqldb
                nosqlDB.con = Connection(host=nosqlDB.initParas['host'], port=nosqlDB.initParas['port'], max_pool_size=100)
    #             nosqlDB.con = MongoClient(host=nosqlDB.initParas['host'], port=nosqlDB.initParas['port'], max_pool_size=200)
                
                nosqlDB.db = Database(nosqlDB.con, nosqlDB.initParas['db'])
                if nosqlDB.initParas['isauth'] == '1':
                    nosqlDB.db.auth(nosqlDB.initParas['user'], nosqlDB.initParas['passwd'])
                nosqlDB.gfs = GridFS(nosqlDB.db, 'files')
            except BaseException,e:
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
    
    

if __name__ == '__main__':
    
#     dbcon = nosqlDB.getInstance()
#     print dbcon.db.user.insert({'a':threading.current_thread().name})
    
#     def callback():
#         dbcon = nosqlDB.getInstance()
#         print dbcon.db.user.insert({'a':threading.current_thread().name})
#         print threading.current_thread().name
#     for i in range(10):
#         th = Thread(target=callback)
#         th.start()
#         th.join()
    
#     print 'over'
    pass
