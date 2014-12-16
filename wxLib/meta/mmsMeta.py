# -*- encoding: utf-8 -*-
'''
Created on '2014/12/16'

@author: 'hu'
'''
import MySQLdb

#
# Base = declarative_base()
#
#
# class MMSMessage(Base):
# __tablename__ = 'api_mt_BBB'
# mobiles = Column('mobiles', String(255))
# content = Column('content', String(255))
# is_wap = Column('is_wap', Integer)


def getMMSDBConn():
    conn = MySQLdb.connect(host="59.57.246.61", user="OATEST", passwd="123456789", db="mas")
    return conn


if __name__ == '__main__':
    pass