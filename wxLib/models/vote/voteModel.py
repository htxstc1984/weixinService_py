# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''

from wxLib.meta.vote.voteMeta import *
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

class Vote_schema(Vote_schema_meta):
    items = db.relationship('Vote_item')

class Vote_item(Vote_item_meta):
    schema_id = db.relationship(db.Column(db.Integer,db.ForeignKey('vote_schema.id')))
    actions = db.relationship('Vote_action')

class Vote_action(Vote_action_meta):
    item_id = db.relationship(db.Column(db.Integer,db.ForeignKey('vote_item.id')))

if __name__ == '__main__':

    from wxLib.db import mysqlDB

    schemas = mysqlDB.getSession().query(Vote_schema)

    pass