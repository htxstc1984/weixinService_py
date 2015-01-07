# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''
from globalVars import *
from flask import session
from flask.templating import render_template
from json import *
from flask import make_response
from flask import request
from werkzeug.wrappers import Response, Headers
from werkzeug.utils import secure_filename
import simplejson
from wxLib.meta.weixinMeta import *
from wxLib.utils import *
from wxLib.callws.ehr import *
from sqlalchemy import and_, or_, func
import os


@app.route('/heka')
def getHeka():
    return render_template('vote/mobi/heka1.html')


@app.route('/voteSetting')
def voteSetting():
    return render_template('vote/setting.html')


@app.route('/getTree', methods=['GET', 'POST'])
def getschematree():
    schemas = wx_session.query(Vote_schema).all()
    resp = make_response(createTree(schemas))
    assert isinstance(resp, Response)
    resp.headers = Headers({'Content-type': 'application/json'})
    return resp


@app.route('/schema/view/<schema_id>', methods=['GET', 'POST'])
def getVoteItems(schema_id=None):
    schema = wx_session.query(Vote_schema).filter_by(id=schema_id).one()
    return render_template('vote/schemaView.html', schema=schema)


@app.route('/schema/add', methods=['GET', 'POST'])
def schemaAdd():
    schema = Vote_schema()
    schema.fromDate = datetime.utcnow()
    schema.toDate = datetime.utcnow()
    return render_template('vote/schemaEdit.html', schema=schema)


@app.route('/schema/edit/<schema_id>', methods=['GET', 'POST'])
def schemaEdit(schema_id=None):
    schema = wx_session.query(Vote_schema).filter_by(id=schema_id).one()
    return render_template('vote/schemaEdit.html', schema=schema)


@app.route('/schema/save', methods=['GET', 'POST'])
def saveSchema():
    schema = Vote_schema.getStrInstance(db, **request.form)
    schema.creator = u'htx'
    schema.lastDate = unicode(datetime.utcnow())
    if (schema.id == None):
        schema.createDate = unicode(datetime.utcnow())

    if request.files and request.files['picurl']:
        f = request.files['picurl']
        fname = str(datetime.utcnow().strftime('%Y%M%d_%H%M%S%f')) + f.filename[
                                                                     f.filename.rfind('.'):]  # 获取一个安全的文件名，且仅仅支持ascii字符；
        f.save(ROOT_PATH + UPLOAD_FOLDER + fname)
        schema.picurl = UPLOAD_FOLDER + fname
    wx_session.merge(schema)
    wx_session.commit()
    return "{'sucess':true}"


@app.route('/item/add/<schema_id>')
def addItem(schema_id=None):
    item = Vote_item(schema_id=schema_id)
    return render_template('vote/itemEdit.html', item=item)


@app.route('/item/edit/<itemid>')
def getItem(itemid=None):
    item = wx_session.query(Vote_item).filter_by(id=itemid).one()
    return render_template('vote/itemEdit.html', item=item)


@app.route('/item/save', methods=['GET', 'POST'])
def saveItem():
    item = Vote_item.getStrInstance(db, **request.form)
    if request.files and request.files['picurl']:
        f = request.files['picurl']
        fname = str(datetime.utcnow().strftime('%Y%M%d_%H%M%S%f')) + f.filename[
                                                                     f.filename.rfind('.'):]  # 获取一个安全的文件名，且仅仅支持ascii字符；
        f.save(ROOT_PATH + UPLOAD_FOLDER + fname)
        item.picurl = UPLOAD_FOLDER + fname
    wx_session.merge(item)
    wx_session.commit()
    return "{'sucess':true}"


@app.route('/showImage/<schema_id>')
def showImage(schema_id=None):
    schema = wx_session.query(Vote_schema).filter_by(id=schema_id).one()
    return render_template('common/showImage.html', src=schema.picurl)


@app.route('/mobi/vote/<schema_id>/<openid>')
def getVote(schema_id=None, openid=None):
    if openid == None or openid == '':
        if session.has_key('openid'):
            openid = session.get('openid')
        else:
            return render_template('vote/error.html', title=u'错误', message=u'无法确认您的微信身份')
    session['openid'] = openid
    rs = checkOpenid(openid)
    psnname = ''
    mobile = ''
    bz = ''
    isregisted = False
    if rs['resultCode'] == 0:
        psnname = rs['psnname']
        mobile = rs['mobile']
        isregisted = True

    psn_detail = wx_session.query(Vote_psn_detail).filter(
        and_(Vote_psn_detail.schema_id == schema_id, Vote_psn_detail.openid == openid)).all()

    if len(psn_detail) != 0:
        psnname = psn_detail[0].psnname
        mobile = psn_detail[0].mobile
        bz = psn_detail[0].bz

    schema = wx_session.query(Vote_schema).filter_by(id=schema_id).one()
    if schema == None:
        return render_template('vote/error.html', title=u'错误', message=u'您选择的投票不存在')
    items = wx_session.query(Vote_item, Vote_action.item_id).outerjoin(Vote_action,
                                                                       and_(Vote_action.item_id == Vote_item.id,
                                                                            Vote_action.openid == openid)).filter(
        and_(Vote_item.schema_id == schema.id)).all()
    return render_template('vote/mobi/vote.html', schema=schema, openid=openid, items=items, psnname=psnname,
                           mobile=mobile, bz=bz, isregisted=isregisted)


@app.route('/mobi/vote/submit', methods=['POST'])
def submitVote():
    if not session.has_key('openid'):
        return render_template('vote/error.html', title=u'错误', message=u'无法确认您的微信身份')
    try:
        openid = session['openid']

        data = request.data
        json = simplejson.loads(data)

        schema_id = json['schema_id']
        psnname = json['psnname']
        mobile = json['mobile']
        bz = json['bz']

        psn_detail = Vote_psn_detail(openid=openid, schema_id=schema_id, psnname=psnname, mobile=mobile, bz=bz)
        wx_session.merge(psn_detail)

        actions = list()

        for selectItem in json['selectItems']:
            action = Vote_action(openid=json['openid'], item_id=int(selectItem), schema_id=json['schema_id'],
                                 voteDate=unicode(datetime.utcnow()))
            actions.append(action)

        oldactions = wx_session.query(Vote_action).filter(
            and_(Vote_action.openid == openid, Vote_action.schema_id == json['schema_id'])).all()

        for oldaction in oldactions:
            wx_session.delete(oldaction)

        wx_session.add_all(actions)
        wx_session.commit()
        return str(openid)
    except BaseException, e:
        print e.message
        return 'error'


def makeUrl(src):
    return 'http://' + ROOT_PATH + src


def createTree(schemas):
    root = dict({"id": 'root', "text": "全部投票", "state": "closed"})
    schemas_list = list()
    for schema in schemas:
        assert isinstance(schema, Vote_schema)
        schema_dict = dict()
        schema_dict['id'] = schema.id
        schema_dict['text'] = schema.schemaname
        schema_dict['attributes'] = sa_obj_to_dict(schema)
        schemas_list.append(schema_dict)
    root['children'] = schemas_list
    return str(dumps([root], cls=CJsonEncoder))


if __name__ == '__main__':
    pass