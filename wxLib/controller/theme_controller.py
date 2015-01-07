# -*- encoding: utf-8 -*-
'''
Created on '2014/12/18'

@author: 'hu'
'''

from globalVars import *
from flask import session
from flask.templating import render_template
from flask import make_response
from flask import request, url_for, redirect
from werkzeug.wrappers import Response, Headers
from wxLib.meta.weixinMeta import *
from wxLib.callws.ehr import *


@app.route('/collect/<int:collect_id>/main/<openid>')
def getTheme(collect_id=None, openid=None):
    collect = wx_session.query(Theme_collection).filter(Theme_collection.id == collect_id).one()
    if collect == None:
        return render_template('common/error.html', title=u'错误', message=u'找不到此页面')
    now = unicode(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if now > collect.expire:
        return render_template('common/error.html', title=u'提示', message=u'活动已经过期')
    if not session.has_key('openid'):
        session['openid'] = openid
    return render_template('theme/collection/' + collect.template_dir + '/main.html', title=collect.title,
                           collect_id=collect_id)


@app.route('/collect/<int:collect_id>/addCollect')
def getAddCollectPage(collect_id=None):
    if not session.has_key('openid'):
        return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份或者session过期，请退出重试')
    openid = session['openid']
    collect = wx_session.query(Theme_collection).filter(Theme_collection.id == collect_id).one()
    if collect == None:
        return render_template('error.html', title=u'错误', message=u'找不到此页面')
    psn = checkOpenid(openid)
    return render_template('theme/collection/' + collect.template_dir + '/addCollect.html', title=collect.title,
                           collect_id=collect_id, openid=openid, psn=psn)


@app.route('/collect/<int:collect_id>/add/<openid>', methods=['POST'])
def addCollect(collect_id=None, openid=None):
    if not session.has_key('openid'):
        return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份或者session过期，请退出重试')
    psnname = request.form['psnname']
    mobile = request.form['mobile']
    content = request.form['content']
    createDate = unicode(datetime.utcnow())
    item = Theme_collection_item(collect_id=collect_id, openid=openid, psnname=psnname, mobile=mobile, content=content,
                                 createDate=createDate)
    try:
        wx_session.add(item)
        wx_session.commit()
        return 'success'
    except BaseException, e:
        print e.message
        return 'error'


@app.route('/collect/<int:collect_id>/list/<openid>')
def collectList(collect_id=None, openid=None):
    collect = wx_session.query(Theme_collection).filter(Theme_collection.id == collect_id).one()
    if collect == None:
        return render_template('common/error.html', title=u'错误', message=u'找不到此页面')
    if not session.has_key('openid'):
        return render_template('common/error.html', title=u'错误', message=u'无法确认您的微信身份或者session过期，请退出重试')
    list = wx_session.query(Theme_collection_item).filter(
        and_(Theme_collection_item.collect_id == collect_id, Theme_collection_item.openid == openid)).all()
    return render_template('theme/collection/' + collect.template_dir + '/collectList.html', title=u'我的留言', items=list,
                           collect_id=collect_id)


if __name__ == '__main__':
    pass