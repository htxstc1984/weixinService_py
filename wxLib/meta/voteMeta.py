# -*- encoding: utf-8 -*-
'''
Created on '2014/12/3'

@author: 'hu'
'''

from globalVars import *
from wxLib.utils import *


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


if __name__ == '__main__':
    pass