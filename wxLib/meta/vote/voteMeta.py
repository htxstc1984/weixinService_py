# -*- encoding: utf-8 -*-
'''
Created on '2014/12/1'

@author: 'hu'
'''
import os, sys

thePath = os.getcwdu()
thePath = thePath[:thePath.find("weixinService_py\\") + len('weixinService_py')]
sys.path.append(thePath)

from globalVars import *

class Vote_schema(Base,db.Model):
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
    items = db.relationship('Vote_item')


class Vote_item(Base,db.Model):
    __tablename__ = 'vote_item'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    # schema_id = db.Column('schema_id', db.Integer, primary_key=True, nullable=False)
    schema_id = db.Column('schema_id', db.Integer, db.ForeignKey('vote_schema.id'), primary_key=True, nullable=False)
    itemtitle = db.Column('itemtitle', db.Unicode(255), nullable=False)
    itemdesc = db.Column('itemdesc', db.Text, nullable=False)
    actions = db.relationship('Vote_action')


class Vote_action(Base,db.Model):
    __tablename__ = 'vote_action'
    id = db.Column('id', db.Integer, autoincrement=db.Integer, primary_key=True)
    openid = db.Column('openid', db.Integer, nullable=False)
    # itemid = db.Column('itemid', db.Integer, nullable=False)
    item_id = db.Column('item_id', db.Integer, db.ForeignKey('vote_item.id'))
    voteDate = db.Column('voteDate', db.DateTime, nullable=True)


if __name__ == '__main__':
    manager.run()
    pass