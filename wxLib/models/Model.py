# -*- encoding: utf-8 -*-
'''
Created on 2014-11-12

@author: huangtx@itg.net
'''
from wxLib.db import nosqlDB
from bson.objectid import ObjectId
from pymongo.cursor import Cursor

def getDB():
    return nosqlDB.getInstance()

class MetaModel(dict):
    def __init__(self, **kw):
        for k, v in kw.items():
            self[k] = v
    
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, value):
        self[key] = value
        
    @classmethod
    def getDocs(cls, *args, **kw):
        cur = getDB().db[cls.__tablename__].find(*args, **kw)
        return [u for u in cur]
    
    @classmethod
    def getDoc(cls, *args, **kw):
        return getDB().db[cls.__tablename__].find_one(*args, **kw)
    
    def _save2DB(self):
        return getDB().db[self.__tablename__].find_and_modify(query={'_id':self._id}, update=self , upsert=True)
    

class User(MetaModel):
    __tablename__ = 'user'
    
    @classmethod
    def createUser(cls, username, passwd, email, *args, **kw):
        if User.checkUsername(username):
            return (False, u'用户名已经存在')
        try:
            kw.update(dict(_id=ObjectId(), username=username, password=passwd, email=email))
            user = User(**kw)
            user._save2DB()
            return (True, user)
        except BaseException, e:
            print e
            return (False, e)
    @classmethod
    def checkUsername(cls, username):
        return getDB().db[cls.__tablename__].find_one({'username':username})
    
    @classmethod
    def doLogin(cls, username, password):
        user = User.getDoc(dict(username=username, password=password))
        if user:
            return True, user
        else:
            return False, '用户名或密码错误'
    
class Article(MetaModel):
    __tablename__ = 'article'
    @classmethod
    def createArticle(cls, title, content, author, *args, **kw):
        try:
            kw.update(dict(_id=ObjectId(), title=title, content=content, author=author))
            article = Article(**kw)
            article._save2DB()
            return (True, article)
        except BaseException, e:
            print e
            return (False, e)

if __name__ == '__main__':
    
#     rs = User.createUser('htx22', 'htx', '123@123.com')
#     print rs[1]
    
#     user = User.getDoc({'username':'htx'})
#     users = User.getDocs({'username':'htx2'})
#     print users

    rs = Article.createArticle('test', 'htxtest', 'htx')
    print rs[1]
    pass
