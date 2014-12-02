# -*- encoding: utf-8 -*-
'''
Created on '2014/12/1'

@author: 'hu'
'''
import os,sys

thePath = os.getcwdu()
thePath = thePath[:thePath.find("weixinService_py\\") + len('weixinService_py')]
sys.path.append(thePath)

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from conf.globalConf import mysqldb
app = Flask(__name__)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s?charset=utf8' % (
        mysqldb['user'], mysqldb['passwd'], mysqldb['host'], mysqldb['db'])
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
except BaseException, e:
    print e.message


class Vote_schema_meta(db.Model):
    __tablename__ = 'vote_schema'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    schemaname = db.Column('schemaname', db.Unicode(255), nullable=False)
    desc = db.Column('desc', db.Text, nullable=False)
    fromDate = db.Column('fromDate', db.DateTime, nullable=False)
    toDate = db.Column('toDate', db.DateTime, nullable=False)
    createDate = db.Column('createDate', db.DateTime, nullable=False)
    lastDate = db.Column('lastDate', db.DateTime, nullable=True)
    creator = db.Column('creator', db.Unicode(255), nullable=False)
    mutiable = db.Column('mutiable', db.Integer, nullable=False, default=0)


class Vote_item_meta(db.Model):
    __tablename__ = 'vote_item'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    schema_id = db.Column('schema_id', db.Integer, primary_key=True, nullable=False)
    itemtitle = db.Column('itemtitle', db.Unicode(255), nullable=False)
    itemdesc = db.Column('itemdesc', db.Text, nullable=False)


class Vote_action_meta(db.Model):
    __tablename__ = 'vote_action'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    openid = db.Column('openid', db.Integer, nullable=False)
    itemid = db.Column('itemid', db.Integer, nullable=False)
    voteDate = db.Column('voteDate', db.DateTime, nullable=True)


if __name__ == '__main__':
    manager.run()
    pass