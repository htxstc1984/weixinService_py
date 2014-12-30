# -*- encoding: utf-8 -*-
'''
Created on '2014/12/29'

@author: 'hu'
'''

from sqlalchemy import *
from conf.globalConf import *
from sqlalchemy.orm import scoped_session, sessionmaker, query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_, or_, func

engine_ehr = create_engine(SQLALCHEMY_DATABASE_URI_EHR, pool_size=20)
session_ehr = scoped_session(sessionmaker(bind=engine_ehr, autocommit=False, autoflush=False))
Base = declarative_base()


class Weixin_org(Base):
    __tablename__ = 'v_itg_weixin_org'
    ehrid = Column('ehrid', String(30), primary_key=True)
    fatherid = Column('fatherid', String(30))
    deptname = Column('deptname', String(30))
    depttyp = Column('depttyp', String(30))
    ts = Column('ts', String(30))

    def getSimpleDict(self):
        return dict(ehrid=str(self.ehrid).strip(),
                    fatherid=str(self.fatherid).strip(),
                    deptname=self.deptname,
                    depttyp=self.depttyp,
                    ts=self.ts
        )


if __name__ == '__main__':
    # corps = session_ehr.query(Weixin_org).filter(Weixin_org.depttyp == 'corp').all()
    # for corp in corps:
    # print corp.deptname.encode('latin-1').decode('gbk')
    pass