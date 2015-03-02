# -*- encoding: utf-8 -*-
'''
Created on '2014/12/12'

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
from wxLib.callws.ehr import *
from sqlalchemy import and_, or_, func
import os
from encoder import XML2Dict
from conf.weixinMenuConf import *
from xml.dom import minidom
import pycurl, StringIO
import time as sysTime
from sqlalchemy import *
import re

@app.teardown_appcontext
def shutdown_session(exception=None):
    wx_session.remove()
    session_inner.remove()
    session_ehr.remove()
    session_cms.remove()


@app.route('/imageView/<src>')
def getImageView(src=None):
    src = '/static/image/' + src
    return render_template('common/imageView.html', src=src)


@app.route('/summary')
def getSummary():
    return render_template('weixin/location_new.html')


@app.route('/business')
def getBussiness():
    return render_template('weixin/business.html')


@app.route('/links')
def getLinks():
    return render_template('weixin/links.html')


@app.route('/stock')
def getStock():
    return render_template('weixin/stock.html')


@app.route('/news/list/<int:page>')
def getNewsIndex(page=0):
    queryIndex = session_cms.query(SwInfo.infoid, SwInfo.infotitle, SwInfo.infodatetime, SwInfo.columnid).filter(
        and_(SwInfo.infoisdisplay == '1', SwInfo.columnid.in_((2, 3)))).order_by(
        desc(SwInfo.infodatetime)).offset(page * 10).limit(10)
    newsList = queryIndex.all()
    return render_template('weixin/itgNews.html', newsList=newsList, page=page)


@app.route('/news/get/<int:infoid>')
def getNewsBody(infoid=None):
    query = session_cms.query(SwInfo).filter(and_(SwInfo.infoisdisplay == '1', SwInfo.infoid == infoid))
    newsBody = query.one()
    newsBody.infocontent = getRightHtml(newsBody.infocontent)
    return render_template('weixin/newsView.html', newsBody=newsBody)


@app.route('/register/<openid>')
def getRegister(openid=None):
    if openid == None or openid == '':
        return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份')
    session['openid'] = openid
    return render_template('weixin/register.html')


@app.route('/reg/submit', methods=['POST'])
def confirmRegister():
    if session.has_key('openid'):
        openid = session['openid']
    else:
        return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份或者session过期，请刷新页面重试')
    cond = request.form['cond']
    type = request.form['type']
    code = bindWeixin(cond, type, openid)
    ret = ''
    if type == 'mms':
        if code > 999999:
            print code
            msg = sendmms(cond, str(code))
            if msg == 'success':
                ret = dumps(dict(code=0, type='mms', msg='绑定成功'))
            else:
                ret = dumps(dict(code=999, type='mms', msg=msg))
        else:
            ret = dumps(dict(code=code, msg=errors['e' + str(code)]))

    if type == 'email':
        if code == 0:

            ret = dumps(dict(code=0, type='email', msg='已经向您的国贸邮箱发送认证邮件，请进入邮箱确认!'))
        else:
            ret = dumps(dict(code=code, msg=errors['e' + str(code)]))

    resp = make_response(ret)
    assert isinstance(resp, Response)
    resp.headers = Headers({'Content-type': 'application/json'})
    return resp


@app.route('/reg/checkmms', methods=['POST'])
def checkmms():
    if not session.has_key('openid') or not request.form.has_key('mmscode'):
        return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份或者session过期，请刷新页面重试')
    openid = session['openid']
    mmscode = request.form['mmscode']
    retcode = confirmBindMMS(mmscode, openid)
    return str(retcode)


@app.route('/reg/checkemail/<uid>')
def checkemail(uid=None):
    return render_template('weixin/checkemail.html', code=uid)


@app.route('/reg/email/bind/<code>')
def bindemail(code=None):
    rs = confirmBind(code)
    if rs == 0:
        return render_template('common/error.html', title=u'温馨提示', message=u'欢迎您，请使用微信平台为国贸员工定制的信息服务！')
    else:
        return render_template('common/error.html', title=u'错误', message=u'验证失败，您的邮件可能已经过期，请重新认证')


@app.route('/reg/delete', methods=['POST'])
def deleteRegister():
    if not session.has_key('openid'):
        return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份或者session过期，请刷新页面重试')
    openid = session['openid']
    code = unbindWeixin(openid)
    return str(code)


def sendmms(phone, mmscode):
    try:
        conn = getMMSDBConn()
        msg = u'您的国贸微信平台认证码是：' + unicode(mmscode[1:len(mmscode)]) + u',请在微信平台输入此验证码.'
        sql = "insert into api_mt_BBB(mobiles,content,is_wap) values('%s','%s',0) " % (str(phone), msg.encode('gb2312'))
        print sql
        cursor = conn.cursor()
        n = cursor.execute(sql)
        print n
        conn.commit()
        cursor.close()
        conn.close()
        return 'success'
    except BaseException, e:
        print e.message
        return e.message


@app.route('/itg/menus/<openid>')
def getMenusNS(openid=None):
    if session.has_key('openid'):
        session.pop('openid')
    rs = checkOpenid(openid)
    if rs['resultCode'] != 0:
        return redirect(url_for('getRegister', openid=openid))
    session['openid'] = openid
    return render_template('weixin/menus.html', openid=openid)


@app.route('/itg/menus')
def getMenus():
    if not session.has_key('openid'):
        return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份或者session过期，请刷新页面重试')
    openid = session['openid']
    rs = checkOpenid(openid)
    if rs['resultCode'] != 0:
        return redirect(url_for('getRegister', openid=openid))
    return render_template('weixin/menus.html', openid=openid)


@app.route('/itg/query')
def getQuery():
    if not session.has_key('openid'):
        return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份或者session过期，请刷新页面重试')
    return render_template('weixin/query.html')


@app.route('/itg/query/get', methods=['POST'])
def getPsnInfos():
    if not session.has_key('UserId'):
        if not session.has_key('openid'):
            return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份或者session过期，请刷新页面重试')
        cond = request.form['cond']
        openid = session['openid']
        rs = checkOpenid(openid)
        if rs['resultCode'] != 0:
            return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份')
    else:
        cond = request.form['cond']
        openid = 'oGWhot6q83jPLENglsitEv1xjYCw'
    rs_psn = getPsnPhoneVOs(openid, cond)
    resp = make_response(dumps(rs_psn))
    assert isinstance(resp, Response)
    resp.headers = Headers({'Content-type': 'application/json'})
    return resp


@app.route('/weixinrec', methods=['GET', 'POST'])
def weixinrec():
    if request.method == 'GET':
        return request.args.get('echostr')
    xml2dict = XML2Dict(coding='utf-8')
    xml = xml2dict.parse(request.data)
    vo = xml['xml']

    if vo.has_key('MsgType'):
        if vo['MsgType'] == 'text':
            if testCommand.has_key(vo['Content']):

                retUrl = '没有对应的返回值'
                v = str(testCommand[vo['Content']])
                if (v.find('%s') != -1):
                    retUrl = str(testCommand[vo['Content']]) % vo['FromUserName']
                else:
                    retUrl = str(testCommand[vo['Content']])

                retXML = ''
                retXML += '<xml>'
                retXML += '<ToUserName><![CDATA[' + vo['FromUserName'] + ']]></ToUserName>'
                retXML += '<FromUserName><![CDATA[' + vo['ToUserName'] + ']]></FromUserName>'
                retXML += '<CreateTime>' + str(int(sysTime.time() * 1000)) + '</CreateTime>'
                retXML += '<MsgType><![CDATA[text]]></MsgType>'
                retXML += '<Content><![CDATA[' + retUrl + ']]></Content>'
                retXML += '</xml>'
                retXML = retXML.replace('&lt;', '<').replace('&gt;', '>')
                return retXML

    if vo.has_key('Event') and vo.has_key('EventKey'):
        if vo['Event'] == 'subscribe':
            retXML = ''
            retXML += '<xml>'
            retXML += '<ToUserName><![CDATA[' + vo['FromUserName'] + ']]></ToUserName>'
            retXML += '<FromUserName><![CDATA[' + vo['ToUserName'] + ']]></FromUserName>'
            retXML += '<CreateTime>' + str(int(sysTime.time() * 1000)) + '</CreateTime>'
            retXML += '<MsgType><![CDATA[text]]></MsgType>'
            retXML += '<Content><![CDATA[欢迎关注厦门国贸！]]></Content>'
            retXML += '</xml>'
            retXML = retXML.replace('&lt;', '<').replace('&gt;', '>')
            return retXML
        if vo['Event'] == 'CLICK':
            doc = minidom.Document()
            root = doc.createElement('xml')
            doc.appendChild(root)
            toUserName = doc.createElement('ToUserName')
            toUserName.appendChild(doc.createTextNode('<![CDATA[' + vo['FromUserName'] + ']]>'))
            root.appendChild(toUserName)

            fromUserName = doc.createElement('FromUserName')
            fromUserName.appendChild(doc.createTextNode('<![CDATA[' + vo['ToUserName'] + ']]>'))
            root.appendChild(fromUserName)

            createTime = doc.createElement('CreateTime')
            createTime.appendChild(doc.createTextNode(str(int(sysTime.time() * 1000))))
            root.appendChild(createTime)

            msgType = doc.createElement('MsgType')
            msgType.appendChild(doc.createTextNode('<![CDATA[news]]>'))
            root.appendChild(msgType)

            articles = doc.createElement('Articles')

            for k, group in groups.iteritems():
                if group['name'] == vo['EventKey']:
                    menuHeader = doc.createElement('item')
                    headerTitle = doc.createElement('Title')
                    headerTitle.appendChild(doc.createTextNode('<![CDATA[' + group['title'] + ']]>'))
                    menuHeader.appendChild(headerTitle)

                    headerPicUrl = doc.createElement('PicUrl')
                    headerPicUrl.appendChild(doc.createTextNode('<![CDATA[' + group['picurl'] + ']]>'))
                    menuHeader.appendChild(headerPicUrl)

                    articles.appendChild(menuHeader)
                    articleNum = 1
                    for k, menu in menus.iteritems():
                        if menu['group'] == group:
                            menuitem = doc.createElement('item')

                            itemTitle = doc.createElement('Title')
                            itemTitle.appendChild(doc.createTextNode('<![CDATA[' + menu['title'] + ']]>'))
                            menuitem.appendChild(itemTitle)

                            itemUrl = doc.createElement('Url')
                            itemUrl.appendChild(
                                doc.createTextNode('<![CDATA[' + (menu['url'] % vo['FromUserName']) + ']]>'))
                            menuitem.appendChild(itemUrl)

                            itemPicUrl = doc.createElement('PicUrl')
                            itemPicUrl.appendChild(doc.createTextNode('<![CDATA[' + menu['picurl'] + ']]>'))
                            menuitem.appendChild(itemPicUrl)

                            articles.appendChild(menuitem)
                            articleNum = articleNum + 1

                    articleCount = doc.createElement('ArticleCount')
                    articleCount.appendChild(doc.createTextNode(str(articleNum)))
                    root.appendChild(articleCount)
                    root.appendChild(articles)
                    xml = str(doc.toxml())
                    # xml = pickle.loads(xml)
                    xml = xml.replace('&lt;', '<').replace('&gt;', '>')
                    return xml
    return 'error'


def createButtons():
    token = getAccessToken(APP_ID, SECRET)
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        curl.setopt(pycurl.URL, "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + token)
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        post_data = dumps(buttons, ensure_ascii=False)
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



def getAccessToken(app_id, secret):
    curl = pycurl.Curl()
    f = StringIO.StringIO()
    curl.setopt(pycurl.URL, "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="
                + app_id + "&secret=" + secret)
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


def getRightHtml(content):
    rgExp1 = re.compile("(<[Ii][Mm][Gg].+?src=['|\"](?!http))")
    items = rgExp1.findall(content)
    items = set(items)
    for item in items:
        content = rgExp1.sub(item + u'http://www.itg.com.cn', content)
    rgExp2 = re.compile("(<v:imagedata.+?src[\\s]*=[\\s]*['|\"](?!http))")
    items = rgExp2.findall(content)
    items = set(items)
    for item in items:
        content = rgExp2.sub(item + u'http://www.itg.com.cn', content)
    return content


if __name__ == '__main__':
    # createButtons()
    pass