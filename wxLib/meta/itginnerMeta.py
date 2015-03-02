# -*- encoding: utf-8 -*-
'''
Created on '2015/2/4'

@author: 'hu'
'''

from sqlalchemy import *
from conf.globalConf import *
from sqlalchemy.orm import scoped_session, sessionmaker, query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_, or_, func

engine_inner = create_engine(SQLALCHEMY_DATABASE_URI_INNER, pool_size=50, max_overflow=100)
session_inner = scoped_session(sessionmaker(bind=engine_inner, autocommit=False, autoflush=False))
Base = declarative_base()


class kfolder(Base):
    __tablename__ = 'kfolder'
    id = Column('id', Integer, primary_key=True)
    foldername = Column('foldername', String(50))

    def getSimpleDict(self):
        return dict(id=self.id,
                    foldername=self.foldername.encode('latin-1').decode('gbk')
        )


class kfile(Base):
    __tablename__ = 'kfile'
    id = Column('id', Integer, primary_key=True)
    fatherid = Column('fatherid', String(50))
    title = Column('title', Text)
    showflag = Column('showflag', String(1))
    content = Column('content', Text)
    founddate = Column('founddate', String(50))
    foundtime = Column('foundtime', String(50))

    def getSimpleDict(self):
        return dict(id=self.id,
                    fatherid=self.fatherid,
                    title=self.title.encode('latin-1').decode('gbk'),
                    showflag=str(self.showflag).strip(),
                    content=self.content.encode('latin-1').decode('gbk'),
                    founddate=str(self.founddate).strip(),
                    foundtime=str(self.foundtime).strip()
        )


if __name__ == '__main__':
    # kfiles = session_inner.query(kfile).order_by(kfile.founddate.desc()).limit(10).all()
    # for file in kfiles:
    # print file.content
    pass