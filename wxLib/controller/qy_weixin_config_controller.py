# -*- encoding: utf-8 -*-
'''
Created on '2014/12/29'

@author: 'hu'
'''
from werkzeug.urls import url_decode
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
import re
import copy
from collections import namedtuple
from urllib import urlencode
from wxLib.weixin.WXBizMsgCrypt import WXBizMsgCrypt
from wxLib.weixin.common import *
import xml.etree.cElementTree as ET
import time as sysTime
from werkzeug.utils import redirect
from wxLib.callws.ehr import *
from wxLib.func.qy_weixin_operator import *


@app.route('/qy/app/5/main')
def getCommunity():
    return render_template('weixin/qy/gmdcommunity.html')


@app.route('/qy/test/getpsn')
def getPsnInfo():
    code = request.args.get('code')
    agentid = request.args.get('state')
    ret = getPsnInfoByCode(code, agentid)
    if ret.has_key('UserId'):
        app.logger.info(ret['UserId'])
        app.logger.info(ret['DeviceId'])
        return ret['UserId']
    else:
        app.logger.info(ret['errcode'])
        app.logger.info(ret['errmsg'])
        return ret['errmsg']


@app.route('/qy/app/3/main')
def getQyQuery():
    if not session.has_key('UserId'):
        code = request.args.get('code')
        agentid = request.args.get('state')
        if code == None or agentid == None:
            return render_template('common/error.html', title=u'错误', message=u'无法确认您的身份或者session过期，请刷新页面重试')
        ret = getPsnInfoByCode(code, agentid)
        if ret.has_key('UserId'):
            session['UserId'] = ret['UserId']
        else:
            return render_template('common/error.html', title=u'错误', message=u'无法确认您的身份或者session过期，请刷新页面重试')

    if session.has_key('UserId'):
        return render_template('weixin/query.html')


@app.route('/qy/app/4/main/<int:page>')
def getInnerInfo(page=0):
    # print str(session_inner.bind.engine.pool._overflow)
    # kfiles = session_inner.query(kfile.fatherid, kfolder.foldername, kfile.title,
    # kfile.founddate, kfile.id).join(kfolder, kfile.fatherid == kfolder.id).filter(
    # kfile.showflag == 'Y').order_by(kfile.founddate.desc()).offset(
    # page * 10).limit(10).all()
    #
    # newsList = []
    # for file in kfiles:
    # news = {}
    # news['foldername'] = file[1].encode('latin-1').decode('gbk')
    #     news['title'] = file[2].encode('latin-1').decode('gbk')
    #     news['founddate'] = file[3]
    #     news['id'] = file[4]
    #     newsList.append(news)
    #     print str(session_inner.bind.engine.pool._overflow)
    # return render_template('weixin/qy/itgInnerNews.html', newsList=newsList, page=page)

    if not session.has_key('UserId'):
        code = request.args.get('code')
        agentid = request.args.get('state')
        if code == None or agentid == None:
            return render_template('common/error.html', title=u'错误', message=u'无法确认您的身份或者session过期，请刷新页面重试')
        ret = getPsnInfoByCode(code, agentid)
        if ret.has_key('UserId'):
            session['UserId'] = ret['UserId']
        else:
            return render_template('common/error.html', title=u'错误', message=u'无法确认您的身份或者session过期，请刷新页面重试')

    if session.has_key('UserId'):
        kfiles = session_inner.query(kfile.fatherid, kfolder.foldername, kfile.title,
                                     kfile.founddate, kfile.id).join(kfolder, kfile.fatherid == kfolder.id).filter(
            kfile.showflag == 'Y').order_by(kfile.founddate.desc(), kfile.id.desc()).offset(page * 10).limit(10).all()

        newsList = []
        for file in kfiles:
            news = {}
            news['foldername'] = file[1].encode('latin-1').decode('gbk')
            news['title'] = file[2].encode('latin-1').decode('gbk')
            news['founddate'] = file[3]
            news['id'] = file[4]
            newsList.append(news)

        return render_template('weixin/qy/itgInnerNews.html', newsList=newsList, page=page,
                               username=session['UserId'])

    else:
        return ret['errmsg']


@app.route('/qy/app/4/view/<int:infoid>')
def getInnerInfoView(infoid=None):
    if not session.has_key('UserId'):
        code = request.args.get('code')
        agentid = request.args.get('state')
        if code == None or agentid == None:
            return render_template('common/error.html', title=u'错误', message=u'无法确认您的身份或者session过期，请刷新页面重试')
        ret = getPsnInfoByCode(code, agentid)
        if ret.has_key('UserId'):
            session['UserId'] = ret['UserId']
        else:
            return render_template('common/error.html', title=u'错误', message=u'无法确认您的身份或者session过期，请刷新页面重试')
    news = session_inner.query(kfile).filter(kfile.id == infoid).all()
    if len(news) > 0:
        newsBodys = convert_result_to_chinese(news, kfile)
        newsBody = newsBodys[0]
        if newsBody['fatherid'] in newsFolderExt:
            newsBody['content'] = u'该栏目的信息请您在PC端登陆内网查看!'
    else:
        newsBody = None

    innerhit = wx_session.query(InnerNews_hits).filter(InnerNews_hits.id == infoid).first()
    if innerhit == None:
        innerhit = InnerNews_hits()
        innerhit.id = infoid
        innerhit.hits = 1
        wx_session.merge(innerhit)
    else:
        innerhit.hits += 1
        wx_session.merge(innerhit)
    wx_session.commit()
    return render_template('weixin/qy/innernewsView.html', newsBody=newsBody, username=session['UserId'],
                           hits=innerhit.hits)


@app.route('/qy/main/<root>')
def getMainPage(root=None):
    root_corp_name = ''
    if root == '1001':
        root_corp_name = u'国贸集团股份有限公司'
    else:
        root_corp = session_ehr.query(Weixin_org).filter(Weixin_org.ehrid == root).one()
        if not root_corp == None:
            root_corp = root_corp.getSimpleDict()
            root_corp_name = root_corp['deptname']
    return render_template('weixin/qy/main.html', root_corp_name=root_corp_name, root_id=root)


@app.route('/qy/manage/<org_id>', methods=['POST'])
def getManageOrgs(org_id=None):
    orgs = session_ehr.query(Weixin_org).filter(Weixin_org.fatherid == org_id).order_by(Weixin_org.depttyp,
                                                                                        Weixin_org.ehrid).all()
    rs_orgs = convert_result_to_chinese(orgs, Weixin_org)
    resp = make_response(dumps(rs_orgs))
    assert isinstance(resp, Response)
    resp.headers = Headers({'Content-type': 'application/json'})
    return resp


@app.route('/qy/app/all/subscribe', methods=['GET', 'POST'])
def qyAppSubscribe():
    sReqMsgSig = request.args.get('msg_signature')
    sReqTimeStamp = request.args.get('timestamp')
    sReqNonce = request.args.get('nonce')

    if request.method == 'GET':
        # wxcpt = WXBizMsgCrypt(TOKEN_QY, AESKEY_QY, APP_ID_QY)
        ret, sEchoStr = wxcpt.VerifyURL(url_decode(request.query_string)['msg_signature'],
                                        url_decode(request.query_string)['timestamp'],
                                        url_decode(request.query_string)['nonce'],
                                        url_decode(request.query_string)['echostr'])
        # print ret

        return sEchoStr

    # app.logger.info(request.data)
    # app.logger.info(sReqMsgSig)
    # app.logger.info(sReqTimeStamp)
    # app.logger.info(sReqNonce)

    ret, decodeXML = getDecryptMsg(request.data, sReqMsgSig, sReqTimeStamp, sReqNonce)
    # app.logger.info(str(ret))
    # app.logger.info(decodeXML)
    if decodeXML:
        userid = decodeXML.find("FromUserName").text
        my = decodeXML.find("ToUserName").text
        app.logger.info(userid)
        msgType = decodeXML.find("MsgType").text
        if msgType == 'event':
            event = decodeXML.find("Event").text
            if event == 'subscribe':
                userid = decodeXML.find("FromUserName").text
                detail = getPsnDetail(userid)
                if detail.has_key('weixinid'):
                    psn = wx_session.query(Document_psn).filter(Document_psn.qywxid == userid).first()
                    psn.weixinid = detail['weixinid']
                    wx_session.merge(psn)
                    wx_session.commit()

                retXML = ''
                retXML += '<xml>'
                retXML += '<ToUserName><![CDATA[' + userid + ']]></ToUserName>'
                retXML += '<FromUserName><![CDATA[' + my + ']]></FromUserName>'
                retXML += '<CreateTime>' + str(int(sysTime.time() * 1000)) + '</CreateTime>'
                retXML += '<MsgType><![CDATA[text]]></MsgType>'
                retXML += '<Content><![CDATA[欢迎关注国贸集团企业号,获取公司内部网信息，增进交流，提升工作效率。]]></Content>'
                retXML += '</xml>'
                retXML = retXML.replace('&lt;', '<').replace('&gt;', '>')

                ret, sEncryptMsg = wxcpt.EncryptMsg(retXML, sReqNonce, sReqTimeStamp)

                return sEncryptMsg

    return ''


@app.route('/qy/app/4/receive', methods=['GET', 'POST'])
def qyApp4receive():
    sReqMsgSig = request.args.get('msg_signature')
    sReqTimeStamp = request.args.get('timestamp')
    sReqNonce = request.args.get('nonce')

    if request.method == 'GET':
        # wxcpt = WXBizMsgCrypt(TOKEN_QY, AESKEY_QY, APP_ID_QY)
        ret, sEchoStr = wxcpt.VerifyURL(url_decode(request.query_string)['msg_signature'],
                                        url_decode(request.query_string)['timestamp'],
                                        url_decode(request.query_string)['nonce'],
                                        url_decode(request.query_string)['echostr'])
        # print ret

        return sEchoStr

    ret, decodeXML = getDecryptMsg(request.data, sReqMsgSig, sReqTimeStamp, sReqNonce)
    if decodeXML:
        userid = decodeXML.find("FromUserName").text
        my = decodeXML.find("ToUserName").text

        msgType = decodeXML.find("MsgType").text
        app.logger.info(msgType)
        if msgType == 'event':
            event = decodeXML.find("Event").text
            app.logger.info(event)
            if event == 'enter_agent' or event == 'click':
                userid = decodeXML.find("FromUserName").text
                kfiles = session_inner.query(kfile.fatherid, kfolder.foldername, kfile.title,
                                             kfile.founddate, kfile.id).join(kfolder,
                                                                             kfile.fatherid == kfolder.id).filter(
                    kfile.showflag == 'Y').order_by(kfile.founddate.desc(), kfile.id.desc()).limit(5).all()

                newsList = []
                newsList.append({'title': '点击打开完整内网信息：', 'url': makeSafeUrl('http://59.57.246.46/qy/app/4/main/0'),
                                 'picurl': 'http://59.57.246.46/static/image/logo4.jpg'})
                num = 1
                for file in kfiles:
                    news = {}
                    news['title'] = str(file[2].encode('latin-1').decode('gbk'))
                    news['url'] = makeSafeUrl('http://59.57.246.46/qy/app/4/view/' + str(file[4]))
                    news['picurl'] = 'http://59.57.246.46/static/image/num-' + str(num) + '.png'
                    newsList.append(news)
                    num += 1

                # newsList.append({'title': '查看所有内网新闻>>>', 'url': makeSafeUrl('http://59.57.246.46//qy/app/4/main/0'),
                # 'picurl': 'http://59.57.246.46/static/image/gmgl2.png'})

                msgdata = {
                    "touser": userid,
                    "msgtype": "news",
                    "agentid": "4",
                    "news": {
                        "articles": newsList
                    }
                }
                app.logger.info(dumps(msgdata, ensure_ascii=False))
                retData = sendMsgToUser(msgdata)
                app.logger.info(retData['errmsg'])

                retXML = ''
                retXML += '<xml>'
                retXML += '<ToUserName><![CDATA[' + userid + ']]></ToUserName>'
                retXML += '<FromUserName><![CDATA[' + my + ']]></FromUserName>'
                retXML += '<CreateTime>' + str(int(sysTime.time() * 1000)) + '</CreateTime>'
                retXML += '<MsgType><![CDATA[text]]></MsgType>'
                retXML += '<Content><![CDATA[]]></Content>'
                retXML += '</xml>'
                retXML = retXML.replace('&lt;', '<').replace('&gt;', '>')

                ret, sEncryptMsg = wxcpt.EncryptMsg(retXML, sReqNonce, sReqTimeStamp)

                return sEncryptMsg

    return ''


@app.route('/qy/app/3/receive', methods=['GET', 'POST'])
def qyApp3receive():
    sReqMsgSig = request.args.get('msg_signature')
    sReqTimeStamp = request.args.get('timestamp')
    sReqNonce = request.args.get('nonce')

    if request.method == 'GET':
        # wxcpt = WXBizMsgCrypt(TOKEN_QY, AESKEY_QY, APP_ID_QY)
        ret, sEchoStr = wxcpt.VerifyURL(url_decode(request.query_string)['msg_signature'],
                                        url_decode(request.query_string)['timestamp'],
                                        url_decode(request.query_string)['nonce'],
                                        url_decode(request.query_string)['echostr'])
        # print ret

        return sEchoStr

    retXML = ''

    ret, decodeXML = getDecryptMsg(request.data, sReqMsgSig, sReqTimeStamp, sReqNonce)
    if decodeXML:
        userid = decodeXML.find("FromUserName").text
        my = decodeXML.find("ToUserName").text

        retXML += '<xml>'
        retXML += '<ToUserName><![CDATA[' + userid + ']]></ToUserName>'
        retXML += '<FromUserName><![CDATA[' + my + ']]></FromUserName>'
        retXML += '<CreateTime>' + str(int(sysTime.time() * 1000)) + '</CreateTime>'
        retXML += '<MsgType><![CDATA[text]]></MsgType>'
        retXML += '<Content><![CDATA[%s]]></Content>'
        retXML += '</xml>'
        retXML = retXML.replace('&lt;', '<').replace('&gt;', '>')

        msgType = decodeXML.find("MsgType").text
        if msgType == 'text':
            content = decodeXML.find("Content").text
            if content != '':
                userid = decodeXML.find("FromUserName").text
                app.logger.info(content)
                ret = getPsnPhoneVOs(u'oGWhot6q83jPLENglsitEv1xjYCw', content)
                if ret['code'] != 0:
                    retXML = retXML % ret['msg'].encode('utf-8')
                else:
                    rsMsg = ''
                    for psn in ret['psn']:
                        rsMsg += '【' + str(psn['psnname']) + '】\n'
                        rsMsg += ((psn['email'] == 'null' or psn['email'] == '') and '' or (
                            u'\U00002709'.encode('utf-8') + str(psn['email']) + '\n'))
                        if (psn['yglb'] != "0001V410000000001OPY"):
                            rsMsg += ((psn['officephone'] == 'null' or psn['officephone'] == '') and '' or (
                                u'\U0000260E'.encode('utf-8') + str(psn['officephone']) + '\n'))
                            rsMsg += ((psn['mobile'] == 'null' or psn['mobile'] == '') and '' or (
                                u'\U0001F4F1'.encode('utf-8') + str(psn['mobile']) + '\n'))

                    retXML = retXML % rsMsg

    ret, sEncryptMsg = wxcpt.EncryptMsg(retXML, sReqNonce, sReqTimeStamp)

    return sEncryptMsg




@app.route('/qy/manage/fromehr/syq')
def getSyqFromEhr():
    try:
        syqs = session_ehr.query(Weixin_syq).all()
        rs_syqs = convert_result_to_chinese(syqs, Weixin_syq)
        for i, syq in enumerate(rs_syqs):
            dept = Document_dept()
            dept.syqcode = syq['syqcode']
            dept.deptname = syq['syqname']
            dept.fatherid = '1'
            dept.order = str(i + 1)
            wx_session.merge(dept)

        wx_session.commit()
        return u'事业群数据更新完成'
    except BaseException, e:
        return u'获取事业群数据失败'


@app.route('/qy/manage/toqywx/syq')
def pushSyqToQyWeixin():
    try:
        syqs = wx_session.query(Document_dept).all()
        for i, syq in enumerate(syqs):
            assert isinstance(syq, Document_dept)
            if syq.qywxid != None:
                orgdata = dict(name=syq.deptname, parentid='1', order=str(syq.order), id=syq.qywxid)
            else:
                orgdata = dict(name=syq.deptname, parentid='1', order=str(syq.order))
            ret = createOrg(orgdata)
            if ret['errcode'] == 0:
                if syq.qywxid == None:
                    syq.qywxid = str(ret['id'])
                    wx_session.merge(syq)
            else:
                print '微信返回失败：' + ret['errmsg']
        wx_session.commit()
        return u'事业群数据更新完成'
    except BaseException, e:
        return u'获取事业群数据失败'


@app.route('/qy/manage/fromehr/psn')
def getPsnsBySyq():
    try:

        # last_psn_ids = session_ehr.query(Weixin_syq_psn.psncode).order_by(Weixin_syq_psn.psncode).all()
        # last_idset = set([x for x in last_psn_ids])

        exist_psn_ids = wx_session.query(Document_psn).order_by(Document_psn.psncode).all()
        exist_idset = {x.psncode: x for x in exist_psn_ids}

        syqs = wx_session.query(Document_dept).filter(Document_dept.qywxid != '').all()
        for i, syq in enumerate(syqs):
            corps = session_ehr.query(Weixin_syq_corp).filter(Weixin_syq_corp.syqcode == syq.syqcode).all()
            rs_corps = convert_result_to_chinese(corps, Weixin_syq_corp)
            for corp in rs_corps:
                print u'--' + corp['unitcode'] + '||' + corp['unitname']
                psns = session_ehr.query(Weixin_syq_psn).filter(
                    Weixin_syq_psn.unitcode.like(corp['unitcode'] + '%')).all()
                rs_psns = convert_result_to_chinese(psns, Weixin_syq_psn)
                for psn in rs_psns:
                    wxpsn = Document_psn()
                    wxpsn.psncode = psn['psncode']
                    wxpsn.psnname = psn['psnname']
                    wxpsn.department = syq.deptname
                    wxpsn.departmentid = syq.qywxid
                    wxpsn.mobile = psn['mobile']
                    wxpsn.email = psn['email']
                    wxpsn.officephone = psn['officephone']
                    wxpsn.unitname = psn['unitname']
                    wxpsn.deptname = psn['deptname']
                    wxpsn.ehrid = psn['basid']

                    if exist_idset.has_key(wxpsn.psncode):
                        existpsn = exist_idset[wxpsn.psncode]
                        if existpsn.qywxid != None:
                            wxpsn.isexist = '1'
                        else:
                            wxpsn.isexist = '0'

                        olddetail = str(existpsn.departmentid) + str(existpsn.mobile) + str(existpsn.email) + str(
                            existpsn.officephone) + str(existpsn.deptname)
                        newdetail = syq.qywxid + str(psn['mobile']) + str(psn['email']) + str(psn['officephone']) + str(
                            psn['deptname'])
                        if olddetail == newdetail and existpsn.needrefresh == '0':
                            wxpsn.needrefresh = '0'
                        else:
                            wxpsn.needrefresh = '1'

                    else:
                        wxpsn.isexist = '0'
                        wxpsn.needrefresh = '1'

                    # print u'----' + psn['psnname'] + '||' + psn['unitcode'] + '||' + psn['unitname']
                    wx_session.merge(wxpsn)
            wx_session.commit()
        return u'获取员工信息成功'
    except BaseException, e:
        wx_session.rollback()
        return u'获取员工信息失败'


@app.route('/qy/manage/toqywx/psn/delete')
def deletePsnToQyWeixin():
    try:
        last_psn_ids = session_ehr.query(Weixin_syq_psn.psncode).order_by(Weixin_syq_psn.psncode).all()
        last_idset = set([x[0] for x in last_psn_ids])

        dellist = {'useridlist': []}
        delpsns = []

        exist_psns = wx_session.query(Document_psn).filter(Document_psn.isexist == '1').all()
        for psn in exist_psns:
            if psn.psncode not in last_idset:
                dellist['useridlist'].append(psn.psncode)
                delpsns.append(psn)

        if len(dellist['useridlist']) > 0:
            pass
            ret = deletePsnBat(dellist)
            if ret['errcode'] == 0:
                for delpsn in delpsns:
                    wx_session.delete(delpsn)

                wx_session.commit()
            else:
                return ret['errmsg']

        return u'获取员工信息成功'
    except BaseException, e:
        wx_session.rollback()
        return u'获取员工信息失败'


@app.route('/qy/manage/toqywx/psn')
def pushPsnToQyWeixin():
    p = None
    try:
        psns = wx_session.query(Document_psn).filter(
            or_(Document_psn.isexist == '0', Document_psn.needrefresh == '1')).all()
        # psns = wx_session.query(Document_psn).filter(Document_psn.psncode == '301490').all()
        for i, psn in enumerate(psns):
            print i
            p = psn
            assert isinstance(psn, Document_psn)
            type = 'create'
            psndata = {}
            psndata['name'] = psn.psnname
            psndata['department'] = [psn.departmentid]

            if len(psn.mobile) == 11:
                psndata['mobile'] = psn.mobile
            if psn.email.encode('utf-8').find('@') > 0:
                psndata['email'] = psn.email
            if psn.qywxid != None:
                psndata['userid'] = psn.qywxid
                type = 'update'
            else:
                psndata['userid'] = psn.psncode

            psndata['extattr'] = {}
            psndata['extattr']['attrs'] = [{'name': '公司', 'value': str(psn.unitname)},
                                           {'name': '部门', 'value': str(psn.deptname)},
                                           {'name': '办公电话', 'value': str(psn.officephone)}]

            ret = createPsn(psndata, type)
            if ret['errcode'] == 0:
                if psn.qywxid == None:
                    psn.qywxid = psn.psncode

                psn.needrefresh = '0'
                psn.isexist = '1'
                wx_session.merge(psn)
            elif ret['errcode'] == 60106:
                psndata.pop('email')
                ret2 = createPsn(psndata, type)
                if ret2['errcode'] == 0:
                    if psn.qywxid == None:
                        psn.qywxid = psn.psncode
                    psn.needrefresh = '0'
                    psn.isexist = '1'
                    wx_session.merge(psn)
                else:
                    log = Document_log()
                    log.type = 'psn'
                    log.successflag = '1'
                    log.content = psn.psnname.encode('utf-8') + '|' + ret['errmsg'].encode('utf-8')
                    log.ts = str(datetime.now())
                    wx_session.add(log)
                    print  ret['errmsg']
            else:
                log = Document_log()
                log.type = 'psn'
                log.successflag = '1'
                log.content = psn.psnname.encode('utf-8') + '|' + ret['errmsg'].encode('utf-8')
                log.ts = str(datetime.now())
                wx_session.add(log)
                print  ret['errmsg']
        wx_session.commit()

        return u'人员数据更新完成'
    except BaseException, e:
        wx_session.commit()
        return u'获取人员数据失败'


@app.route('/qy/manage/toqywx/psn/delall')
def deleteAllPsns():
    try:
        psns = wx_session.query(Document_psn).filter(Document_psn.qywxid != '').all()
        useridlist = {'useridlist': []}
        for psn in psns:
            useridlist['useridlist'].append(psn.qywxid)
        rs = deletePsnBat(useridlist)
        return rs['errmsg']
    except BaseException, e:
        raise e


@app.route('/admin/eEdit/uploadfile/<rq>/<fname>', methods=['GET', 'POST'])
def getstaticfilefrominner(rq=None, fname=None):
    buf = StringIO.StringIO()
    buf_header = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://www.itg.net/admin/eEdit/uploadfile/' + rq + '/' + fname)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.HEADERFUNCTION, buf_header.write)
    c.perform()
    c.close()
    resp = make_response(buf.getvalue())
    assert isinstance(resp, Response)
    ret_header = buf_header.getvalue()
    header_items = ret_header.split('\r\n')
    for item in header_items:
        if item.find('Content-Type') != -1:
            resp.headers = Headers({'Content-type': item.split(':')[1]})
    return resp





if __name__ == '__main__':
    pass