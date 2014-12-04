# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from conf.globalConf import SQLALCHEMY_DATABASE_URI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, query
import os

ROOT_PATH = os.path.dirname(__file__)
UPLOAD_FOLDER = '/static/files/'
try:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    db = SQLAlchemy(app)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=db.engine))
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    Base = declarative_base()
    Base.query = db_session.query_property()

except BaseException, e:
    print e.message

if __name__ == '__main__':
    pass