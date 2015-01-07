# -*- encoding: utf-8 -*-
'''
Created on '2014/12/29'

@author: 'hu'
'''
from globalVars import *
from flask import session
from flask.templating import render_template
import json
from flask import make_response
from flask import request, url_for, redirect
from werkzeug.wrappers import Response, Headers
import simplejson
from wxLib.meta.weixinMeta import *
from wxLib.utils import *
from sqlalchemy import and_, or_, func
import os
from encoder import XML2Dict
from conf.weixinMenuConf import *
import pycurl, StringIO
from sqlalchemy import *
from wxLib.meta.ehrMeta import *
import re
import copy


@app.route('/qy/main/<root>')
def getMainPage(root=None):
    root_corp_name = ''
    if root == '1001':
        root_corp_name = u'国贸集团股份有限公司'
    else:
        root_corp = session_ehr.query(Weixin_org).filter(Weixin_org.ehrid == root).one()
        if not root_corp == None:
            root_corp = root_corp.getSimpleDict()
    return render_template('weixin/qy/main.html', root_corp_name=root_corp['deptname'], root_id=root)


@app.route('/qy/manage/<org_id>', methods=['POST'])
def getManageOrgs(org_id=None):
    orgs = session_ehr.query(Weixin_org).filter(Weixin_org.fatherid == org_id).order_by(Weixin_org.depttyp,
                                                                                        Weixin_org.ehrid).all()
    rs_orgs = convert_result_to_chinese(orgs, ['deptname'], Weixin_org)
    resp = make_response(dumps(rs_orgs))
    assert isinstance(resp, Response)
    resp.headers = Headers({'Content-type': 'application/json'})
    return resp


@app.route('/qy/manage/create')
def createOrgTree():
    try:
        orgindexmap = {'1001': '1'}
        orgs = session_ehr.query(Weixin_org).order_by(Weixin_org.fatherid, Weixin_org.depttyp).all()
        rs_orgs = convert_result_to_chinese(orgs, ['deptname'], Weixin_org)
        order = 1
        fatherid = '1001'
        for org in rs_orgs:
            parentid = orgindexmap[org['fatherid']]
            orgdata = dict(name=org['deptname'], parentid=parentid, order=str(order))
            ret = createOrg(orgdata)
            if ret['errcode'] == 0:
                orgindexmap[org['ehrid']] = str(ret['id'])
                doc_dept = Document_dept(deptname=org['deptname'], fatherid=org['fatherid'], ehrid=org['ehrid'],
                                         qywxid=str(ret['id']),
                                         order=str(order))
                wx_session.merge(doc_dept)
            else:
                return '初始化组织架构失败'
            if org['fatherid'] != fatherid:
                fatherid = org['fatherid']
                order = 1
            else:
                order += 1
    except BaseException, e:
        print e.message
        return '初始化组织架构失败'
    wx_session.commit()
    return '初始化组织架构成功'


def convert_result_to_chinese(resultset, fields, Class):
    convertedset = list()
    for field in fields:
        for row in resultset:
            newrow = copy.copy(row)
            # setattr(newrow, field, getattr(newrow, field).encode('latin-1').decode('gbk'))
            convertedset.append(newrow)
    if not Weixin_org.getSimpleDict == None:
        convertedset = [row.getSimpleDict() for row in convertedset]
    return convertedset


def createOrg(org):
    token = getAccessToken(APP_ID_QY, SECRET_QY)
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        curl.setopt(pycurl.URL, "https://qyapi.weixin.qq.com/cgi-bin/department/create?access_token=" + token)
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        post_data = dumps(org, ensure_ascii=False).encode('utf-8')
        curl.setopt(curl.POSTFIELDS, post_data)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        curl.close()
        if backinfo == '':
            print 'error'
        else:
            print backinfo
            return loads(backinfo)


def getAccessToken(app_id, secret):
    curl = pycurl.Curl()
    f = StringIO.StringIO()
    curl.setopt(pycurl.URL, "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + app_id + "&corpsecret=" + secret)
    curl.setopt(pycurl.WRITEFUNCTION, f.write)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.perform()
    backinfo = ''
    if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
        backinfo = f.getvalue()
    curl.close()
    if backinfo == '':
        return False

    result = loads(backinfo)
    return result['access_token']


if __name__ == '__main__':
    pass