# -*- encoding: utf-8 -*-
'''
Created on '2014/12/17'

@author: 'hu'
'''
from sqlalchemy import *
from conf.globalConf import *
from sqlalchemy.orm import scoped_session, sessionmaker, query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_, or_, func

engine_cms = create_engine(SQLALCHEMY_DATABASE_URI_CMS, pool_size=15)
session_cms = scoped_session(sessionmaker(bind=engine_cms, autocommit=False, autoflush=False))
Base = declarative_base()


class SwInfo(Base):
    __tablename__ = 'sw_info'
    infoid = Column('infoid', Integer, primary_key=True)
    infotitle = Column('infotitle', Text)
    infodatetime = Column('infodatetime', String(20))
    infoisdisplay = Column('infoisdisplay', String(1))
    infocontent = Column('infocontent', Text)
    columnid = Column('columnid', Integer)
    infohits = Column('infohits', Integer)


if __name__ == '__main__':
    # cursor = session.execute('select top 100 * from sw_info ORDER by infodatetime DESC ')
    # assert isinstance(cursor,)
    # query = session_cms.query(SwInfo).with_entities(SwInfo.infoid, SwInfo.infotitle, SwInfo.infodatetime).filter(
    # and_(SwInfo.infoisdisplay == '1', SwInfo.columnid.in_((2, 3)))).order_by(
    #     desc(SwInfo.infodatetime)).offset(0).limit(10)
    # result = query.all()
    # for v in result:
    #     print v.infocontent
    pass