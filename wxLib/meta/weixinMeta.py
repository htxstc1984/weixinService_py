# -*- encoding: utf-8 -*-
'''
Created on '2014/12/3'

@author: 'hu'
'''
if __name__ == '__main__':
    import sys, os

    sys.path.insert(0, "C:/developIDE/pycharmWorksapce/weixinService_py")
    sys.path.insert(0, "C:/developIDE/pyenvs/env3/Lib/site-packages")

from wxLib.utils import *
from sqlalchemy.orm import scoped_session, sessionmaker, query
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from conf.globalConf import SQLALCHEMY_DATABASE_URI
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=50)
wx_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
# Base.query = wx_session.query_property()
db = SQLAlchemy()


# def getWXSession():
# return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)


class Vote_schema(db.Model, Base, MetaTransform):
    __tablename__ = 'vote_schema'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    schemaname = db.Column('schemaname', db.Unicode(255), nullable=False)
    desc = db.Column('desc', db.Text, nullable=False)
    fromDate = db.Column('fromDate', db.Unicode(30), nullable=False)
    toDate = db.Column('toDate', db.Unicode(30), nullable=False)
    createDate = db.Column('createDate', db.Unicode(30), nullable=False)
    lastDate = db.Column('lastDate', db.Unicode(30), nullable=True)
    creator = db.Column('creator', db.Unicode(255), nullable=False)
    picurl = db.Column('picurl', db.Unicode(255), nullable=True)
    mutiable = db.Column('mutiable', db.Integer, nullable=False, default=0)
    mutimax = db.Column('mutimax', db.Integer, nullable=False, default=0)
    retry = db.Column('retry', db.Integer, nullable=False, default=1)
    items = db.relationship('Vote_item')

    def getSimpleDict(self):
        return dict(id=self.id,
                    schemaname=self.schemaname,
                    desc=self.desc,
                    fromDate=self.fromDate,
                    toDate=self.toDate,
                    createDate=self.createDate,
                    lastDate=self.lastDate,
                    creator=self.creator,
                    picurl=self.picurl,
                    mutiable=self.mutiable,
                    mutimax=self.mutimax
        )


class Vote_item(db.Model, Base, MetaTransform):
    __tablename__ = 'vote_item'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    schema_id = db.Column('schema_id', db.Integer, db.ForeignKey('vote_schema.id'), primary_key=True, nullable=False)
    itemtitle = db.Column('itemtitle', db.Unicode(255), nullable=False)
    itemdesc = db.Column('itemdesc', db.Text, nullable=False)
    picurl = db.Column('picurl', db.Unicode(255), nullable=True)

    def getSimpleDict(self):
        return dict(id=self.id,
                    schema_id=self.schema_id,
                    itemtitle=self.itemtitle,
                    itemdesc=self.itemdesc,
                    picurl=self.picurl
        )


class Vote_action(db.Model, Base, MetaTransform):
    __tablename__ = 'vote_action'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    openid = db.Column('openid', db.Unicode(30), nullable=False)
    schema_id = db.Column('schema_id', db.Integer, nullable=False)
    item_id = db.Column('item_id', db.Integer, nullable=False)
    voteDate = db.Column('voteDate', db.Unicode(30), nullable=True)

    def getSimpleDict(self):
        return dict(id=self.id,
                    openid=self.openid,
                    item_id=self.item_id,
                    voteDate=self.voteDate
        )


class Vote_psn_detail(db.Model, Base, MetaTransform):
    __tablename__ = 'vote_psn_detail'
    openid = db.Column('openid', db.Unicode(30), nullable=False, primary_key=True)
    schema_id = db.Column('schema_id', db.Integer, nullable=False, primary_key=True)
    psnname = db.Column('psnname', db.String(255), nullable=False)
    mobile = db.Column('mobile', db.String(30), nullable=True)
    bz = db.Column('bz', db.String(255), nullable=True)


class Document_log(db.Model, Base, MetaTransform):
    __tablename__ = 'document_log'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    type = db.Column('type', db.String(255))
    key = db.Column('key', db.String(255))
    content = db.Column('content', db.Text)
    ts = db.Column('ts', db.String(255))
    successflag = db.Column('successflag', db.String(1), nullable=False)


class Document_dept(db.Model, Base, MetaTransform):
    __tablename__ = 'document_dept'
    syqcode = Column('syqcode', String(30), primary_key=True)
    deptname = db.Column('deptname', db.String(255), nullable=False)
    fatherid = db.Column('fatherid', db.String(30), nullable=False)
    order = db.Column('order', db.String(30), nullable=False)
    qywxid = db.Column('qywxid', db.String(30), nullable=False)
    isexist = db.Column('isexist', db.String(1))
    needrefresh = db.Column('needrefresh', db.String(1))


class Document_psn(db.Model, Base, MetaTransform):
    __tablename__ = 'document_psn'
    psncode = Column('psncode', String(30), primary_key=True)
    psnname = db.Column('psnname', db.String(255), nullable=False)
    department = db.Column('department', db.String(255), nullable=True)
    departmentid = db.Column('departmentid', db.String(255), nullable=True)
    position = db.Column('position', db.String(255), nullable=True)
    mobile = db.Column('mobile', db.String(255), nullable=True)
    email = db.Column('email', db.String(255), nullable=True)
    officephone = db.Column('officephone', db.String(255), nullable=True)
    unitname = db.Column('unitname', db.String(255), nullable=True)
    deptname = db.Column('deptname', db.String(255), nullable=True)
    weixinid = db.Column('weixinid', db.String(255), nullable=True)
    qywxid = db.Column('qywxid', db.String(30), nullable=True)
    ehrid = db.Column('ehrid', db.String(30), nullable=False)
    isexist = db.Column('isexist', db.String(1))
    needrefresh = db.Column('needrefresh', db.String(1))
    notinehr = db.Column('notinehr', db.String(1))

class Document_tag(db.Model, Base, MetaTransform):
    __tablename__ = 'document_tag'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    tagname = db.Column('tagname', db.String(70), nullable=False)
    qywxid = db.Column('qywxid', db.String(30), nullable=False)
    source = db.Column('source', db.String(30), nullable=False)
    source_id = db.Column('source_id', db.String(30), nullable=False)


class Document_tag_psn(db.Model, Base, MetaTransform):
    __tablename__ = 'document_tag_psn'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    tag_id = db.Column('tag_id', db.Integer, nullable=False)
    psn_id = db.Column('psn_id', db.Integer, nullable=False)


class Theme_collection(db.Model, Base, MetaTransform):
    __tablename__ = 'theme_collection'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)
    desc = db.Column('desc', db.Text, nullable=False)
    title = db.Column('title', db.String(255), nullable=False)
    template_dir = db.Column('template_dir', db.String(255), nullable=False)
    expire = db.Column('expire', db.Unicode(30), nullable=False)


class Theme_collection_item(db.Model, Base, MetaTransform):
    __tablename__ = 'theme_collection_item'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    collect_id = db.Column('collect_id', db.Integer, db.ForeignKey('theme_collection.id'), primary_key=True,
                           nullable=False)
    openid = db.Column('openid', db.Unicode(30), nullable=False)
    content = db.Column('content', db.Text, nullable=False)
    mobile = db.Column('mobile', db.String(30), nullable=False)
    psnname = db.Column('psnname', db.String(20), nullable=False)
    createDate = db.Column('createDate', db.Unicode(30), nullable=True)


class InnerNews_hits(db.Model, Base, MetaTransform):
    __tablename__ = 'innernews_hits'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    hits = db.Column('hits', db.Integer)


if __name__ == '__main__':
    manager.run()
    pass