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

engine_ehr = create_engine(SQLALCHEMY_DATABASE_URI_EHR, pool_size=50)
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
                    deptname=self.deptname.encode('latin-1').decode('gbk'),
                    depttyp=self.depttyp.encode("utf-8"),
                    ts=self.ts.encode("utf-8")
        )


class Weixin_syq(Base):
    __tablename__ = 'v_itg_weixin_syq'
    syqcode = Column('syqcode', String(30), primary_key=True)
    syqname = Column('syqname', String(30))

    def getSimpleDict(self):
        return dict(syqcode=str(self.syqcode).strip(),
                    syqname=self.syqname.encode('latin-1').decode('gbk')
        )


class Weixin_syq_corp(Base):
    __tablename__ = 'v_itg_weixin_syq_corp'
    syqcode = Column('syqcode', String(30))
    syqname = Column('syqname', String(30))
    pkcorp = Column('pk_corp', String(30))
    unitcode = Column('unitcode', String(30), primary_key=True)
    unitname = Column('unitname', String(30))

    def getSimpleDict(self):
        return dict(pkcorp=str(self.pkcorp).strip(),
                    syqcode=str(self.syqcode).strip(),
                    syqname=self.syqname.encode('latin-1').decode('gbk'),
                    unitcode=str(self.unitcode).strip(),
                    unitname=self.unitname.encode('latin-1').decode('gbk')
        )


class Weixin_syq_psn(Base):
    __tablename__ = 'v_itg_weixin_psn'
    psncode = Column('psncode', String(30), primary_key=True)
    basid = Column('pk_psnbasdoc', String(30))
    psnname = Column('psnname', String(255))
    # department = Column('deptname', String(255))
    mobile = Column('mobile', String(255))
    email = Column('email', String(255))
    officephone = Column('officephone', String(255))
    deptname = Column('deptname', String(255))
    unitcode = Column('unitcode', String(30), primary_key=True)
    unitname = Column('unitname', String(30))

    def getSimpleDict(self):
        return dict(psncode=str(self.psncode).strip(),
                    basid=str(self.basid).strip(),
                    psnname=str(self.psnname),
                    # department=self.department.encode('latin-1').decode('gbk'),
                    mobile=str(self.mobile),
                    email=str(self.email),
                    officephone=str(self.officephone),
                    deptname=str(self.deptname),
                    unitcode=str(self.unitcode).strip(),
                    unitname=str(self.unitname)
        )


if __name__ == '__main__':
    # total = 0
    # syqs = session_ehr.query(Weixin_syq).all()
    # for syq in syqs:
    #     print syq.syqname.encode('latin-1').decode('gbk')
    #     corps = session_ehr.query(Weixin_syq_corp).filter(Weixin_syq_corp.syqcode == syq.syqcode).all()
    #     for corp in corps:
    #         sql = session_ehr.query(Weixin_syq_psn).filter(Weixin_syq_psn.unitcode.like(corp.unitcode + '%'))
    #         psns = session_ehr.query(Weixin_syq_psn).filter(Weixin_syq_psn.unitcode.like(corp.unitcode + '%')).all()
    #         print corp.unitcode
    #         print u'--' + corp.unitcode + '||' + corp.unitname.encode('latin-1').decode('gbk') + u'||共有' + str(
    #             len(psns))
    #         total += len(psns)
    #         # for psn in psns:
    #         #     print u'----' + psn.psnname.encode('latin-1').decode('gbk') + '||'+ psn.unitcode + '||' + psn.unitname.encode(
    #         #         'latin-1').decode('gbk')
    #
    # print u'---------' + u'||共有' + str(total)
    pass