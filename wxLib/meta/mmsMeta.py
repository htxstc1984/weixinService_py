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

    # try:
    #     conn = getMMSDBConn()
    #     msg = u'您的国贸微信平台认证码是：123456,请在微信平台输入此验证码.'
    #     sql = "insert into api_mt_BBB(mobiles,content,is_wap) values('%s','%s',0) " % (str(13950002585), msg.encode('gb2312'))
    #     print sql
    #     cursor = conn.cursor()
    #     n = cursor.execute(sql)
    #     print n
    #     conn.commit()
    #     cursor.close()
    #     conn.close()
    # except BaseException, e:
    #     print e.message

    pass